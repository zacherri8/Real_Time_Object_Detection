from fastapi import FastAPI
from backend.database import engine, SessionLocal
from backend.models import Base, Detection

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"status": "API running"}


# -------------------- POST --------------------
@app.post("/detection")
def add_detection(data: dict):

    db = SessionLocal()

    new_det = Detection(
        object_type=data["object"],
        confidence=data["confidence"],
        track_id=data.get("track_id"),
        bbox=str(data.get("bbox")),
        zone=data.get("zone", "none"),

        # ✅ NEW FIELDS
        entry_count=data.get("entry_count", 0),
        exit_count=data.get("exit_count", 0)
    )

    db.add(new_det)
    db.commit()
    db.close()

    return {"message": "saved"}


# -------------------- GET --------------------
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
            "bbox": d.bbox,
            "zone": d.zone,

            # ✅ NEW FIELDS
            "entry_count": d.entry_count,
            "exit_count": d.exit_count
        })

    db.close()

    return result