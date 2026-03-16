from fastapi import APIRouter, Request
from controller.signup import register


router = APIRouter()

router.post("/register")(register)         
