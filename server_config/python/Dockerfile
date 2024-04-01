FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 6969

CMD [ "python", "notify_api.py" ]
# CMD [ "python", "main.py" ]