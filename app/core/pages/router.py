from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import PlainTextResponse 
from core.features.dellin_api.preorder_pages import PreorderPages

authorized: bool = True # Доступ к приложению после авторизации. Сделать авторизацию через тг, потом в базу закинуть как поле пользователя.
router = APIRouter(prefix="", tags=['root'])
templates = Jinja2Templates(directory='app/templates')

@router.get('/devisangry')
async def angry_dev(request: Request):
    if authorized:
        return templates.TemplateResponse(name='angrydev.html', context={'request': request})
    else:
        raise HTTPException(status_code=403, detail="ERROR 403. FORBIDDEN")
    
    
@router.get('/expdatecalc')
async def expdatecal_page(request: Request):
    if authorized:
        return templates.TemplateResponse(name='expdatecalc.html', context={"request": request})
    else:
        raise HTTPException(status_code=403, detail="ERROR 403. FORBIDDEN")


@router.get('/coa') 
async def coa_page(request: Request):
    if authorized:
        return templates.TemplateResponse(name='coa.html', context={"request": request})
    else:
        raise HTTPException(status_code=403, detail="ERROR 403. FORBIDDEN")


@router.get('/')
async def main_page(request: Request):
    if authorized:
        return templates.TemplateResponse(name='home.html', context={"request": request})
    else:
        raise HTTPException(status_code=403, detail="ERROR 403. FORBIDDEN")

@router.get('/test')
async def test_page(request: Request):
    return templates.TemplateResponse(name='base.html', 
                                      context={
                                          'request': request
                                          })
@router.get('/getpreorders')
async def getpreorders_page(request: Request):
    api: PreorderPages = request.app.state.api_object
    api.check_session()
    return templates.TemplateResponse(name='getpreorders.html', 
                                      context={
                                          'request': request
                                          })

# @router.post('/webhook')
# async def webho(request: Request):
#     print(f'request - {request.query_params}')