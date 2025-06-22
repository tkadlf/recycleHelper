#detect
from ultralytics import YOLO
import numpy as np
import cv2
from typing import Dict, List, Tuple
import base64
from pathlib import Path

model_path = Path(__file__).parent / "best.pt"
model = YOLO(str(model_path))
model.to('cpu')

def detect_objects(image_bytes: bytes) -> Dict[str, List[dict]]:
    # 바이트 → NumPy 배열 → OpenCV BGR 이미지
    nparr = np.frombuffer(image_bytes, np.uint8)
    bgr   = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # YOLO 추론
    results = model(bgr, verbose=False)

    detections = []
    annotated_frame = bgr.copy()
    results[0].plot()

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

            # 박스 좌표
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            color = (0, 255, 0)  # 초록색
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
            label = f"{class_name} {confidence_value:.2f}"
            cv2.putText(annotated_frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
     #이미지 PNG로 인코딩
    success, encoded_image = cv2.imencode('.png', annotated_frame)
    if not success:
        raise RuntimeError("이미지 인코딩 실패")
    
     #Base64 인코딩 (bytes → base64 string)
    img_base64 = base64.b64encode(encoded_image).decode('utf-8')

    return {"results": detections,
            "annotated_image": img_base64}