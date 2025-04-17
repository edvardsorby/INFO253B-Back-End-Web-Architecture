from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    # Request could timeout
    # base_dir = os.path.dirname(os.path.abspath(__file__))
    # csv_path = os.path.join(base_dir, "bt_courses.csv")
    # parse_csv_to_json.parse_csv_to_mongodb(csv_path, "mongodb+srv://rathodvikram44:rathodvikram44@allcourses.l4lqk7e.mongodb.net/", "allcourses", "allcourses")
    return {"message": "Hello World"}
