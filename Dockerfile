FROM python:3.12-alpine

WORKDIR /app

RUN apk add build-base libressl libffi-dev libressl-dev libxslt-dev libxml2-dev xmlsec-dev xmlsec

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "python3", "index.py"]