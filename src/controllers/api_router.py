from fastapi import APIRouter

from controllers import event_controller

router = APIRouter()


print("\n\n\n\n\n\n\n\n\n\n")
print("⚽⚽⚽⚽⚽⚽⚽⚽⚽")

print("⚽⚽⚽⚽⚽⚽⚽⚽⚽")
print("\n\n")

print("APLICACION LEVANTADA")
print("\n\n\n")

router.include_router(event_controller.router, tags=["events"])
