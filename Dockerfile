FROM ubuntu:latest
RUN apt-get update -y
#RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install -y python3-pip
RUN apt install curl -y
#working directory inside docker
WORKDIR /app
# copies everything inside this directory(scd_app) into app folder inside root of docker container
# only requirements is copied first to app folder inside docker
COPY ./requirements.txt /app
 #working directory inside docker
RUN pip3 install -r requirements.txt
# copies everything inside this directory(scd_app) into app folder inside root of docker container
COPY . /app
ENTRYPOINT ["python3"]
CMD ["app.py"]