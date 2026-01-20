from fastapi import FastAPI, APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates

authorized: bool = True # Доступ к приложению после авторизации. Сделать авторизацию через тг, потом в базу закинуть как поле пользователя.
router = APIRouter(prefix="", tags=['root'])
templates = Jinja2Templates(directory='app/templates')

@router.get('/')
async def main_page(request: Request):
    if authorized:
        return templates.TemplateResponse(name='home.html', context={'request': request})
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


@router.get('/test')
async def test_page(request: Request):
    return templates.TemplateResponse(name='base.html', 
                                      context={
                                          'request': request
                                          })