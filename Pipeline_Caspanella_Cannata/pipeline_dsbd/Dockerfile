FROM python:3.10 AS dependencies


WORKDIR /app

RUN pip install --upgrade pip
RUN pip install pandas
COPY . /app
RUN apt-get -y update  && apt-get install -y \
  python3-dev \
  apt-utils \
  python-dev \
  build-essential \
&& rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade setuptools
RUN pip install prometheus-api-client
RUN pip install kafka-python
RUN pip install python-snappy
RUN pip install statsmodels
RUN pip install psycopg2
RUN pip install sqlalchemy
RUN pip install docker
RUN pip install flask
RUN pip install prophet



FROM dependencies AS transform
WORKDIR /app
CMD ["python3", "transform.py"]


FROM dependencies AS extract
WORKDIR /app
CMD ["python3", "extract.py"]


FROM dependencies AS load
WORKDIR /app
CMD ["python3", "load.py"]


FROM dependencies AS data_retrieval_sla
WORKDIR /app
CMD ["python3", "data_retrieval_sla.py"]










