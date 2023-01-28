from fastapi import APIRouter

router = APIRouter()


@router.get("/_/status", status_code=200)
async def get_apiaries():
    """
    Moniroting route to know if the application is healthy
    """
    return {"status": "OK"}
