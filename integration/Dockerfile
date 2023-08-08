 FROM ubuntu:18.04
 
#  RUN  sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
 
 RUN apt-get update -y && \  
     apt-get install -y python3-pip python3-dev vim net-tools 

 WORKDIR /app

 COPY app /app

 RUN pip3 install -r /app/requirements.txt --index https://pypi.tuna.tsinghua.edu.cn/simple

 CMD python3 app.py