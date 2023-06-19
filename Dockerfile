FROM python:3.10.0-slim-bullseye

WORKDIR /TextSummarizer

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8550

CMD ["python", "./main.py"]