from flask import Blueprint
from flask_restx import Api

api_v1_bp = Blueprint("api_v1", __name__)
api = Api(
    api_v1_bp,
    version="1.0",
    title="Project Aegis API",
    description="REST API for meteor impact simulation",
    doc="/docs",
)

# Register namespaces
from .endpoints.neos import ns as neos_ns  # noqa: E402
from .endpoints.simulation import ns as simulation_ns  # noqa: E402

api.add_namespace(neos_ns, path="/neos")
api.add_namespace(simulation_ns, path="/simulate")
