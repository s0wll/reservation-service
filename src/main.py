import sys
from pathlib import Path

from fastapi import FastAPI
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))

from src.routers.table import router as router_table


app = FastAPI()

app.include_router(router_table)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)