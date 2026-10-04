from fastapi import FastAPI

app = FastAPI(title="Cognitive Metrics API")

@app.get("/health")
def health():
    return {"status": "ok"}
