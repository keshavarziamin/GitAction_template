FROM ubuntu:22.04
RUN apt -y update && apt -y upgrade
RUN apt install -y build-essential autoconf make cmake git gcc g++ automake libtool python3 pip
RUN pip install colorama

COPY . /Test-CICD
WORKDIR /Test-CICD

CMD ["python3", "cib.py", "--all"]


