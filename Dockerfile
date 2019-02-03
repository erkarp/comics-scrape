FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apt-get update && apt-get install -y netcat
COPY conf/requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
CMD ["gunicorn", "xkcd.wsgi:application", "--bind", "0.0.0.0:8000"]
