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
<<<<<<< HEAD
    return JSONResponse(content=result)
=======
    return JSONResponse(content=result)
>>>>>>> dd3e6cbc4a7fe61057a036a0857e099bc3d6ab63
