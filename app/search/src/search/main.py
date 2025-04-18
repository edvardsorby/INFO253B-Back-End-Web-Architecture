from contextlib import asynccontextmanager

from fastapi import FastAPI

from search.api.main import api_router
from search.db import close_mongo_connection, connect_to_mongo


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)


@app.get("/")
async def root():
    # Request could timeout
    # base_dir = os.path.dirname(os.path.abspath(__file__))
    # csv_path = os.path.join(base_dir, "bt_courses.csv")
    # parse_csv_to_json.parse_csv_to_mongodb(csv_path, "mongodb+srv://rathodvikram44:rathodvikram44@allcourses.l4lqk7e.mongodb.net/", "allcourses", "allcourses")
    return {"message": "Hello World"}
