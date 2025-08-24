from fastapi import APIRouter
from core.template_engine import execute_template

router = APIRouter()

@router.post("/execute-template")
def execute_template_endpoint(payload):
    return execute_template(payload)
