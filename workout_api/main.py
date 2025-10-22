from fastapi import FastAPI
from workout_api.routers import api_router

app = FastAPI(title="Workout API", description="API for managing workout routines", version="1.0.0")
app.include_router(api_router)
