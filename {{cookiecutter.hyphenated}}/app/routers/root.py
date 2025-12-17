from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates


router: APIRouter = APIRouter()
templates: Jinja2Templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def home_page(request: Request):
    context = {}
    return templates.TemplateResponse(request, 'home/index.html', context=context)