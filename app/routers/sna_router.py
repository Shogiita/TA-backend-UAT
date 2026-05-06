from fastapi import APIRouter, Query
from app.controllers import sna_controller

router = APIRouter(
    prefix="/sna",
    tags=["SNA Visualization"]
)


@router.get("/visualization")
def get_visualization(
    source: str = Query("app", description="app atau instagram"),
    mode: int = Query(1, description="1: User to User, 2: User to Post, 3: Post to Post"),
    limit: int = Query(500, ge=10, le=5000)
):
    return sna_controller.get_visualization(
        source=source,
        mode=mode,
        limit=limit
    )