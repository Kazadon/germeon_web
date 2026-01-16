import uvicorn
from fastapi import FastAPI
from core.pages.router import router as router_endpoints


app = FastAPI()
app.include_router(router=router_endpoints)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host='0.0.0.0', reload=True, port=5500)