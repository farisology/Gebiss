# base slim image
FROM python:3.9-slim

#
WORKDIR /code

# Docker Cache
COPY ./requirements.txt /code/requirements.txt

# installing deps
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN apt-get update && apt-get install -y \
    build-essential
# copy our api
COPY ./app /code/app

# using uvicorn to run our app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]