# Pull base image
FROM python

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code/

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY ./docker/web /code/

EXPOSE 8000