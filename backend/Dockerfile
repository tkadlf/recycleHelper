FROM python:3.10

WORKDIR /app

ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID appuser && useradd -u $UID -g $GID -m appuser

RUN apt-get update && apt-get install -y libgl1

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/add/ /app/backend/add/
COPY static/ /app/static/

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "backend.add.main:app", "--host", "0.0.0.0", "--port", "8000"]

