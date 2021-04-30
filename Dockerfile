FROM python:latest

RUN apt-get update \
    && apt-get install tesseract-ocr -y \
    && apt-get clean \
    && apt-get autoremove

WORKDIR /banannna-inst
COPY . /banannna-inst

RUN pip install -r requirements.txt

CMD ["python","app.py"]