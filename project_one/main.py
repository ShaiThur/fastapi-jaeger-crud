import logging

from fastapi import FastAPI

from routers import app_router
from configs.initializer import run_jaeger

app = FastAPI()
app.include_router(app_router.router)
run_jaeger(app)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
