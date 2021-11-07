FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code

WORKDIR /code
COPY requirements.txt /code/
RUN pip3 install -r requirements.txt
COPY . /code/
COPY ./entrypoint.sh /entrypoint.sh
EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]