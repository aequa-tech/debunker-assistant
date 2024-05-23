FROM ubuntu:22.04
RUN apt-get update
RUN apt-get install -y python3.9
RUN apt-get install -y python3-pip
WORKDIR /app
ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN python3 -m spacy download it_core_news_lg
RUN apt-get install -y python3-whois
ADD . /app
WORKDIR /app/API

RUN python3 initialization4docker.py



CMD ["uvicorn", "main:app", "--host", "10.7.0.3", "--port", "8080"]
