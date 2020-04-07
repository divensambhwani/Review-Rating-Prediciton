# lightweight python
FROM python:3.7-slim

# copy local code to the container image
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# install dependencies
RUN pip install Flask gunicorn healthcheck google-cloud-logging 
RUN pip install http://download.pytorch.org/whl/cpu/torch-1.0.0-cp36-cp36m-linux_x86_64.whl

#Run the flask service on container startup
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 Gunicorn.app