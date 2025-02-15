from datetime import datetime

import uvicorn
from fastapi import FastAPI

from app.api.v1.service_routes import service_routers

app = FastAPI()

# routes
app.include_router(service_routers)
app.state.start_time = datetime.now()


@app.get("/")
async def root():
    return {"message": "Hello World"}


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start()
