from fastapi import FastAPI

app = FastAPI(
    title="Intelligence Dashboard",
    description="Analytics and Intelligence Platform",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {
        "message": "Intelligence Dashboard API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}