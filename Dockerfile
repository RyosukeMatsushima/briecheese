FROM python:3.10

RUN apt-get update && apt-get upgrade -y
RUN pip3 install --upgrade pip setuptools

# OpenCV
RUN apt-get install -y libgl1-mesa-glx
RUN pip3 install opencv-python

# scipy
RUN apt-get install -y libopenblas-dev cmake gfortran
RUN pip3 install scipy

# pandas
RUN pip3 install pandas

# DB
RUN apt-get install -y python3-dev default-libmysqlclient-dev && apt-get clean
RUN pip3 install mysqlclient
