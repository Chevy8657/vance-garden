from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from brokerage_data import load_brokerage_records

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/clients")
def clients_page(request: Request):

    records = load_brokerage_records()

    return templates.TemplateResponse(
        request=request,
        name="clients.html",
        context={
            "records": records[::-1]
        }
    )
