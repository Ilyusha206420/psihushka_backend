from fastapi import APIRouter

dialog_router = APIRouter(prefix="/dialog", tags=["dialog"])

@dialog_router.post("/")
def next():
    ...
