from fastapi import FastAPI
from backend.database import engine, SessionLocal
from backend.models import Base, Detection

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"status": "API running"}

@app.post("/detection")
def add_detection(data: dict):

    db = SessionLocal()

    new_det = Detection(
        object_type=data["object_type"],
        confidence=data["confidence"],
        track_id=data.get("track_id"),
        bbox=str(data.get("bbox"))
    )

    db.add(new_det)
    db.commit()
    db.close()

    return {"message": "saved"}

@app.get("/detections")
def get_detections():

    db = SessionLocal()

    detections = db.query(Detection).all()

    result = []

    for d in detections:
        result.append({
            "id": d.id,
            "object": d.object_type,
            "confidence": d.confidence,
            "track_id": d.track_id,
            "bbox": d.bbox
        })

    db.close()

    return result