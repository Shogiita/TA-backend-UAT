from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import test_neo4j_connection
from app.routers import report_router, sna_router

app = FastAPI(
    title="SNA Lite UAT API",
    description="Backend FastAPI untuk website UAT Social Network Analysis menggunakan dummy data Neo4j.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(report_router.router)
app.include_router(sna_router.router)


@app.get("/")
def root():
    return {
        "status": "success",
        "message": "SNA Lite UAT API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "success",
        "api": "running",
        "neo4j": test_neo4j_connection()
    }