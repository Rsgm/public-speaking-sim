###############################
# Speakeazy django server
#
# This file builds the django server container.
# This container is used for both the webserver and the celery worker servers.
#
###############################
FROM


# Set virtualenv environment variables. This is equivalent to running
# source /env/bin/activate
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH


ADD requirements.txt /app/
RUN pip install -r requirements.txt

ADD . /app/

CMD /gunicorn.sh
