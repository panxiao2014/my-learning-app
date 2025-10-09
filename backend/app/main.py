from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.config import TEST_PING

app = FastAPI(title="my-learning-app API")

# Allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, restrict to your domain
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
async def ping():
    return {"message": TEST_PING}