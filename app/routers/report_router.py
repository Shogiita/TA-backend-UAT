from fastapi import APIRouter, Query
from app.controllers import report_controller

router = APIRouter(
    prefix="/report",
    tags=["Report Dashboard"]
)


@router.get("/dashboard")
def get_dashboard():
    return report_controller.get_dashboard_summary()


@router.get("/instagram-profile")
def get_instagram_profile():
    return report_controller.get_instagram_profile()


@router.get("/top-content")
def get_top_content(
    source: str = Query("app", description="app atau instagram"),
    limit: int = Query(10, ge=1, le=100)
):
    return report_controller.get_top_content(source=source, limit=limit)


@router.get("/top-hashtags")
def get_top_hashtags(
    source: str = Query("app", description="app atau instagram"),
    limit: int = Query(10, ge=1, le=100)
):
    return report_controller.get_top_hashtags(source=source, limit=limit)

@router.get("/network-analysis")
def get_network_analysis(
    source: str = Query("app", description="app atau instagram"),
    limit: int = Query(1200, ge=100, le=5000),
    top: int = Query(10, ge=1, le=50),
):
    return report_controller.get_network_analysis(
        source=source,
        limit=limit,
        top=top,
    )