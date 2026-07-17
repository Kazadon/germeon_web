from fastapi import APIRouter, HTTPException, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from core.features.dellin_api.preorder_pages import PreorderPages
from core.features.dellin_api.base_dl import BaseDL

authorized: bool = True # Доступ к приложению после авторизации. Сделать авторизацию через тг, потом в базу закинуть как поле пользователя.
router = APIRouter(prefix="", tags=['root'])
templates = Jinja2Templates(directory='app/templates')

@router.get('/')
async def main_page(request: Request):
    if authorized:
        return templates.TemplateResponse(name='home.html', context={"request": request})
    else:
        raise HTTPException(status_code=403, detail="ERROR 403. FORBIDDEN")


@router.get('/devisangry')
async def angry_dev(request: Request):
    if authorized:
        return templates.TemplateResponse(name='angry/angrydev.html', context={'request': request})
    else:
        raise HTTPException(status_code=403, detail="ERROR 403. FORBIDDEN")
    
      
@router.get('/expdatecalc')
async def expdatecal_page(request: Request):
    if authorized:
        return templates.TemplateResponse(name='expdatecalc/index.html', context={"request": request})
    else:
        raise HTTPException(status_code=403, detail="ERROR 403. FORBIDDEN")


@router.get('/coa') 
async def coa_page(request: Request):
    if authorized:
        return templates.TemplateResponse(name='search_coa/index.html', context={"request": request})
    else:
        raise HTTPException(status_code=403, detail="ERROR 403. FORBIDDEN")



async def get_dl_client(request: Request) -> BaseDL:
    return request.app.state.api_object

class PreorderFilter(BaseModel):
    search_date: str = Field(..., description="Дата для фильтрации в формате YYYY-MM-DD")

@router.get('/getpreorders')
async def getpreorders_page(request: Request):
    return templates.TemplateResponse(name='preorders/index.html', 
                                      context={
                                          'request': request
                                          })
    
@router.get('/preorders/search')
async def search_preorders_api(filters: PreorderFilter = Depends(), api: BaseDL = Depends(get_dl_client)):
        preorderpage_obj = PreorderPages(api)
        orders = await preorderpage_obj.get_germeon_orders(filters.search_date)
        return {"success": True, "data": orders}
    
    
    
    
    
    
    
# @router.get('/test')
# async def test_page(request: Request):
#     return templates.TemplateResponse(name='base.html', 
#                                       context={
#                                           'request': request
#                                           })
