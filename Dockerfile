FROM python:3.8-slim-buster

ENV APP_HOME /mutant_api
ENV PORT 8000
WORKDIR $APP_HOME
COPY . ./

RUN pip install -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 4 --worker-class uvicorn.workers.UvicornWorker  --threads 8 api.server:app
