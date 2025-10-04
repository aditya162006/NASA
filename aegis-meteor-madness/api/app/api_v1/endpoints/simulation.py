from flask_restx import Namespace, Resource, fields
from flask import request, url_for
from app.tasks.simulation_tasks import run_full_simulation_task

ns = Namespace("simulate", description="Simulation endpoints")

simulation_params_model = ns.model(
    "SimulationParams",
    {
        "impactorDiameter": fields.Float(required=True, min=10, max=5000),
        "impactorDensity": fields.Integer(required=True),
        "impactVelocity": fields.Float(required=True, min=1, max=72),
        "impactAngle": fields.Float(required=True, min=1, max=90),
        "targetType": fields.String(required=True, enum=[
            "Sedimentary Rock", "Crystalline Rock", "Water"
        ]),
        "targetLat": fields.Float(required=True, min=-90, max=90),
        "targetLon": fields.Float(required=True, min=-180, max=180),
    },
)

start_response = ns.model(
    "StartResponse",
    {
        "task_id": fields.String,
        "status_url": fields.String,
    },
)

status_response = ns.model(
    "StatusResponse",
    {
        "task_id": fields.String,
        "status": fields.String,
        "result": fields.Raw,
    },
)


@ns.route("")
class StartSimulation(Resource):
    @ns.expect(simulation_params_model, validate=True)
    @ns.marshal_with(start_response)
    def post(self):
        params = request.get_json(force=True)
        task = run_full_simulation_task.delay(params)
        return {
            "task_id": task.id,
            "status_url": url_for("api_v1.simulation_status", task_id=task.id, _external=False),
        }


@ns.route("/status/<string:task_id>")
class SimulationStatus(Resource):
    endpoint = "simulation_status"

    @ns.marshal_with(status_response)
    def get(self, task_id: str):
        from app import celery_app
        assert celery_app is not None
        async_result = celery_app.AsyncResult(task_id)
        payload = {
            "task_id": task_id,
            "status": async_result.status,
        }
        if async_result.successful():
            payload["result"] = async_result.result
        return payload
