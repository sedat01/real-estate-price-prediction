FROM ubuntu:22.04

RUN  apt update &&  apt upgrade -y
RUN  apt install software-properties-common -y
RUN  add-apt-repository ppa:deadsnakes/ppa
RUN apt install pip -y
RUN pip3 install pandas
RUN pip3 install sklearn
RUN pip3 install numpy
RUN pip3 install flask[all]
RUN pip3 install joblib
RUN pip3 install flask-expects-json

COPY . /app
WORKDIR /app
CMD python3 ./api/app.py
