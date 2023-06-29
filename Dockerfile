FROM python:3.10

WORKDIR /app

COPY src .

COPY requirements.txt .

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 poppler-utils -y

RUN pip3 install -r requirements.txt

CMD ["python3","-u","src/main.py"]