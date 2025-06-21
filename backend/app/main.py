#main
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .detect import detect_objects

app = FastAPI(title="YOLOv8 Recycle Helper API")

# CORS 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 헬스 체크
@app.get("/")
def read_root():
    return {"message": "API working"}

# 업로드
@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):

    # 파일 형식 검증
    if file.content_type.split("/")[0] != "image":
        raise HTTPException(status_code=400, detail="이미지 파일을 업로드하세요.")
    
    # 읽기
    image_bytes = await file.read()

    # 추론
    try:
        result = detect_objects(image_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"추론 오류: {e}")
    
    # json 응답
    return JSONResponse(content=result)

# detect.py
from ultralytics import YOLO
import numpy as np
import cv2
from typing import Dict, List

modelPath = "app/best.pt"
model = YOLO(modelPath)

def detect_objects(image_bytes: bytes) -> Dict[str, List[dict]]:
    # 바이트 → NumPy 배열 → OpenCV BGR 이미지
    nparr = np.frombuffer(image_bytes, np.uint8)
    bgr   = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # YOLO 추론
    results = model(bgr, verbose=False)

    # 박스 정보 추출
    detections = []
    for r in results:
        for box in r.boxes:
            
            confidence_value = round(box.conf[0].item(), 3)
            class_id = int(box.cls[0])
            class_name = model.names[class_id] if hasattr(model, 'names') and class_id < len(model.names) else str(class_id)

            detections.append({
                "class_id"  : class_id,
                "class_name": class_name,
                "confidence": confidence_value
            })

    return {"results": detections}