FROM python:3.12.3-slim-bookworm

WORKDIR /usr/src/microservice
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app app/

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
