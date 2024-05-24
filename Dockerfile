FROM ubuntu:22.04
RUN apt-get update
RUN apt-get install -y python3.9
RUN apt-get install -y python3-pip
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN python3 -m spacy download it_core_news_lg
RUN apt-get install -y python3-whois
ADD . /




CMD ["uvicorn", "API:app", "--host", "10.12.0.3", "--port", "8080"]
