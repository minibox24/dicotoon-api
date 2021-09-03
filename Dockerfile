FROM python:3.9-slim-buster
EXPOSE 80
WORKDIR /app
COPY . .
RUN apt update && apt install -y gcc
RUN pip install -r requirements.txt
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]