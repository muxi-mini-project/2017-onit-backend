#base image
FROM python:2.7
MAINTAINER anyaliang <anyaliangww@gmail.com>
#environment setting
ENV DEPLOY_PATH /onit_api
#run command in container
RUN mkdir -p $DEPLOY_PATH
WORKDIR $DEPLOY_PATH
#first add requirement.txt to container
ADD requirement.txt requirement.txt
#install
RUN pip install --index-url http://pypi.doubanio.com/simple/ -r requirement.txt --trusted-host=pypi.doubanio.com
#RUN pip install -r requirement.txt
#add all!
Add . .
