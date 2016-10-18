FROM ubuntu:xenial
RUN apt-get update
RUN apt-get -y install git-core python wget
COPY finglonger.py /usr/local/bin/finglonger
COPY requirements.txt /tmp/finglonger-requirements.txt
RUN wget -O /usr/local/share/get-pip.py https://bootstrap.pypa.io/get-pip.py 
RUN python /usr/local/share/get-pip.py
RUN pip install -r /tmp/finglonger-requirements.txt
RUN chmod +x /usr/local/bin/finglonger
VOLUME /tasks      # for tasks repo
VOLUME /finglonger # for config
ENV HOME /finglonger
WORKDIR /tasks
CMD finglonger
