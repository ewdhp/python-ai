from fastapi import APIRouter

router = APIRouter()

@router.get("/results/{id}")
def get_results(id: str):
    # Fetch stored output by id
    return {"id": id, "result": "Not implemented"}
