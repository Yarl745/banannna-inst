import ssl

import instabot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils import logging

from data.config import WEBHOOK_SSL_CERT, WEBHOOK_SSL_PKEY, IP, REDIS_PASS

inst = instabot.Bot(save_logfile=False)

scheduler = AsyncIOScheduler()

# /etc/ssl/certs/ca-certificates.crt
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PKEY)

# for Windows
# pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# for Linux
# sudo apt install tesseract-ocr
