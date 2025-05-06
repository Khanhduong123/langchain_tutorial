from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from fastapi.responses import FileResponse
import os
from fastapi.staticfiles import StaticFiles
import requests
from ice_breaker import ice_break_with
load_dotenv()

app = FastAPI()
app.mount("/template", StaticFiles(directory="template"), name="template")
@app.get("/")
async def index():
    return FileResponse("template/html/index.html")

from fastapi import Request

@app.post("/process")
async def process(request: Request):
    form_data = await request.form()
    name = form_data['name']
    summary, profile_pic_url = ice_break_with(name)
    from fastapi.responses import JSONResponse
    return JSONResponse({
        "summary_and_facts": summary.to_dict(),
        "profile_pic_url": profile_pic_url
    })