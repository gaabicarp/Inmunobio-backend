FROM python:3.8-slim-buster
RUN apt-get update -y && apt-get install -y build-essential
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT ["python"]
CMD ["app.py"]
