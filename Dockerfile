FROM ubuntu:22.04
RUN apt-get -y update
RUN apt-get install -y build-essential autoconf make cmake git gcc g++ automake libtool 
RUN apt-get install -y python3 python3-pip

# install python dependencies
RUN pip3 install colorama

# set the working directory
WORKDIR /Test-CICD
# copy source files to the working directiry
COPY . /Test-CICD

# Build the source code
RUN mkdir build
RUN git submodule update --init --recursive
RUN cmake -S . -B build
RUN cmake --build build

# Test appliction
RUN cd build && ctest
