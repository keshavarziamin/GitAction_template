FROM ubuntu:22.02
RUN apt -y update && apt -y upgrade
RUN apt install -y build-essential autoconf make cmake gcc g++ automake libtool python3

COPY . /Test-CICD
WORKDIR /Test-CICD

CMD python3 cib.py --all


