from fastapi import APIRouter, Request
from controller.login import login, reset_password, protected, logout  

router = APIRouter()

router.post("/login")(login)         
router.post("/reset-password")(reset_password)  
router.get("/protected")(protected)   
router.post("/logout")(logout)         