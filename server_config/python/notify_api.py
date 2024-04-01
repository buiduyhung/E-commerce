import json
import os
from dotenv import load_dotenv
from pathlib import Path
# import configparser
import mysql.connector
import base64
import requests
from datetime import datetime
import telegram
from flask import (
    Flask,
    Response,
    current_app,
    jsonify,
    make_response,
    request,
    render_template,
    redirect,
    session,
    url_for,
)
from minio import Minio
import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

dotenv_path = Path('../../.env')
load_dotenv(dotenv_path=dotenv_path)

info = {
    "endpoint": "s3p.fsicloud.vn:9000",
    "access_key": "fsi",
    "secret_key": "Fsi@2023!@#",
    "secure": False
}

# info = {
#     "endpoint": os.getenv('AWS_ENDPOINT'),
#     "access_key": os.getenv('AWS_ACCESS_KEY_ID'),
#     "secret_key": os.getenv('AWS_SECRET_ACCESS_KEY'),
#     "secure": False
# }

client = Minio(**info)
app = Flask(__name__)
# telegram_token = os.getenv('TELEGRAM_TOKEN')
telegram_token = '5811832075:AAH6RCnveRJv9nhr4-SR77t4SpoXrt-r34A'
bot = telegram.Bot(telegram_token)


@app.route('/tele', methods=['GET', 'POST'])
def tele():
    if request.method == 'POST':
        rs =request.json
        print(rs)
        chat_id = rs['chat_id']
        mes = rs['content']
        path = 'notify'
        if rs['type'] == 'face_detect':
            path = 'recognition/match'
        # url = f'https://api.telegram.org/bot{telegram_token}/sendMessage'
        client.fget_object("testbucket", f"{path}/{rs['image']}", "latest.jpg")
        for c in chat_id:
            print(c)
            with open("latest.jpg", 'rb') as photo_file:
                bot.sendPhoto(c, photo_file,caption=mes)
        resp = {}
        resp['code'] = 200
        resp['message'] = "Thông báo thành công"
        return  json.dumps(resp, ensure_ascii=False).encode('utf8')
    else:
        resp['code'] = 400
        resp['message'] = "Phương thúc gọi không đúng"
        return  json.dumps(resp, ensure_ascii=False).encode('utf8')

@app.route('/mail', methods=['GET', 'POST'])
def mail():
    if request.method == 'POST':
        rs =request.json
        client.fget_object("testbucket", f"/notify/{rs['image']}", "email.jpg")
        with open("email.jpg", "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())   
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            "attachment; filename= email.jpg",
        )
        subject = "FSI Cloud Camera thông báo"
        body = rs['content']
        sender = "tklamk123@gmail.com"
        recipients = ",".join(rs['chat_id'])
        password = "saoo unuk ldlp zxuv"

        message = MIMEMultipart()
        message["From"] = sender
        message["To"] = recipients
        message["Subject"] = subject

        # Add body to email
        message.attach(MIMEText(body, "plain"))
        message.attach(part)
        text = message.as_string()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipients, text)
        resp = {}
        resp['code'] = 200
        resp['message'] = "Thông báo thành công"
        return  json.dumps(resp, ensure_ascii=False).encode('utf8')
    else:
        resp['code'] = 400
        resp['message'] = "Phương thúc gọi không đúng"
        return  json.dumps(resp, ensure_ascii=False).encode('utf8')

@app.errorhandler(404)
def page_not_found(error):
    mess={}
    mess['Code'] = "E04"
    mess["Message"] ="URL sai hoặc không tồn tại"
    return json.dumps(mess, ensure_ascii=False).encode('utf8')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6969)
