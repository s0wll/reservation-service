import sys
from pathlib import Path

from fastapi import FastAPI
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))

from src.routers.table import router as router_table
from src.routers.reservation import router as router_reservation


app = FastAPI()

app.include_router(router_table)
app.include_router(router_reservation)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)