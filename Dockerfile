FROM python:3.8-slim-buster

RUN apt-get update && \
    apt-get install --yes

RUN pip3 install --upgrade pip
RUN pip3 install virtualenv

RUN virtualenv -p python3 /appenv

ENV PATH=/appenv/bin:$PATH

RUN useradd --create-home --shell /bin/bash app_user

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x run.py

USER app_user

CMD ["bash"]