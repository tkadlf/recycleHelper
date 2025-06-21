#main
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .detect import detect_objects
from fastapi.responses import PlainTextResponse
from pathlib import Path

app = FastAPI(title="YOLOv8 Recycle Helper API")

# CORS 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BACK_FILES  = ["app/main.py", "app/detect.py"]

def read_files(file_list):
    contents = []
    for fp in file_list:
        p = Path(fp)
        if p.exists():
            contents.append(f"# ===== {p.name} =====\n" + p.read_text(encoding="utf-8"))
    return "\n\n".join(contents)

@app.get("/code/backend", response_class=PlainTextResponse)
def show_backend():
    return read_files(BACK_FILES)

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
