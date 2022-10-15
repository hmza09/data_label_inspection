FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHON_VERSION 3
ENV AZURE_STORAGE_CONNECTION_STRING ""

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8501

COPY crowdsourcing_app.py /app
COPY ./tutorials/* /app/tutorials/
COPY ./pages/* /app/pages/


ENTRYPOINT ["streamlit", "run"]

CMD ["crowdsourcing_app.py"]