FROM python:3.10.6

WORKDIR /app

RUN apt-get update && apt-get install -y zip

COPY requirements.txt .

RUN pip config set global.trusted-host 'files.pythonhosted.org pypi.org'
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 8080

CMD ["python", "server.py"]
