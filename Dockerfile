FROM ubuntu:latest
RUN apt-get update -y
#RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install -y python3-pip
RUN apt install curl -y
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["app.py"]