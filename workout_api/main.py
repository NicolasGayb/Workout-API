from fastapi import FastAPI

app = FastAPI(title="Workout API", description="API for managing workout routines", version="1.0.0")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level='info', reload=True)
    
