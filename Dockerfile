from python:3.7

RUN pip install deta fastapi uvicorn

EXPOSE 80

COPY ./app ./app

CMD ["uvicorn", "app.main:app", "host", "0.0.0.0", "--port", "80"]


