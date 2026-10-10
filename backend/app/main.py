from fastapi import FastAPI
    
app = FastAPI(
    title="Ripple API",
    description="Disruption Simulation and Recovery Platform",
    version="0.1.0"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to Ripple API",
        "version": app.version
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }