FROM python:3.8

LABEL maintainer "Bulut Bulgu <bbulgu16@ku.edu.tr>"

RUN apt-get update

RUN mkdir /app

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP flaskiburada.py

EXPOSE 5000

ENTRYPOINT ["python3", "flaskiburada.py", "-host", "0.0.0.0"]