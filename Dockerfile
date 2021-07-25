FROM python 
EXPOSE  8080
RUN apt-get update -y && apt-get install -y build-essential
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app

CMD ["python" , "app.py"]

CMD python -m gunicorn -w 4 -b 0.0.0.0:8080 app:app

