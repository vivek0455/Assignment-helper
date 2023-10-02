
from typing import Union

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import gradio as gr

from gradio_ui import demo

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app = gr.mount_gradio_app(app, demo, '/assistant-bot')

@app.get("/", response_class=HTMLResponse)
def home(request: Request ):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/step1", response_class=HTMLResponse)
def step1_funct(request: Request ):
    return templates.TemplateResponse("step1.html", {"request": request})

@app.get("/step2-q1", response_class=HTMLResponse)
def step2q1_funct(request: Request ):
    return templates.TemplateResponse("step2-q1.html", {"request": request})

@app.get("/step2-q2", response_class=HTMLResponse)
def step2q2_funct(request: Request ):
    return templates.TemplateResponse("step2-q2.html", {"request": request})

@app.get("/step2-q3", response_class=HTMLResponse)
def step2q3_funct(request: Request ):
    return templates.TemplateResponse("step2-q3.html", {"request": request})
@app.get("/step3", response_class=HTMLResponse)
def step3_funct(request: Request ):
    return templates.TemplateResponse("step3.html", {"request": request})

@app.get("/end", response_class=HTMLResponse)
def end(request: Request ):
    return templates.TemplateResponse("end.html", {"request": request})

