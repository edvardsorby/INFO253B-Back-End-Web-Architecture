from fastapi import Depends, FastAPI
from src.dependencies import require_admin

app = FastAPI()

# Example use:
# Include Authorization header with JWT token in the request
#
# Algorithm: HS256
# Secret: your-secret
# Payload:
# {
#     "sub": "admin_user",
#     "role": "admin"
# }
@app.get("/admin")
async def admin_endpoint(user=Depends(require_admin)):
    return {"message": "This endpoint is protected"}

@app.get("/hello")
async def hello():
    return {"message": "This endpoint is not protected"}

