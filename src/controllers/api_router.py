from fastapi import APIRouter

from controllers import event_controller

router = APIRouter()


router.include_router(event_controller.router, tags=["events"])
