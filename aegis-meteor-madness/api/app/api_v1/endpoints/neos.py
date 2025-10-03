from flask_restx import Namespace, Resource, fields
from flask import request
from datetime import datetime

from app.data.nasa_api_service import NasaApiService

ns = Namespace("neos", description="Near-Earth Objects endpoints")

neo_summary = ns.model(
    "NeoSummary",
    {
        "id": fields.String(required=True),
        "name": fields.String(required=True),
        "estimated_diameter_m": fields.Raw(required=True),
        "close_approach_date": fields.String(required=True),
    },
)

neo_list_response = ns.model("NeoListResponse", {"neos": fields.List(fields.Nested(neo_summary))})


@ns.route("")
class NeoList(Resource):
    @ns.response(200, "Success", neo_list_response)
    @ns.response(400, "Bad Request")
    def get(self):
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        try:
            if start_date:
                datetime.strptime(start_date, "%Y-%m-%d")
            if end_date:
                datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            ns.abort(400, "Invalid date format. Use YYYY-MM-DD")

        service = NasaApiService()
        data = service.fetch_neos_by_date_range(start_date, end_date)
        return {"neos": data}


@ns.route("/<string:asteroid_id>")
class NeoDetail(Resource):
    @ns.response(200, "Success")
    @ns.response(404, "Not Found")
    def get(self, asteroid_id: str):
        service = NasaApiService()
        neo = service.fetch_neo_by_id(asteroid_id)
        if neo is None:
            ns.abort(404, "NEO not found")
        return neo
