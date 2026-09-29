FROM python:3.14-alpine

WORKDIR /app
COPY alldebrid.py cache.py server.py ./

CMD ["python", "server.py"]
