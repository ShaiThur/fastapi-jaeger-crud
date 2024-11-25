import logging

import uvicorn
from fastapi import FastAPI

from routers import app_db_router
from configs.initializer import run_jaeger

app = FastAPI()
run_jaeger(app)
app.include_router(app_db_router.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
