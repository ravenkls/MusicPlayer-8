FROM python:3.8

WORKDIR /usr/src/app
COPY . .

RUN set -x \
    && apt-get update \
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:mc3man/trusty-media \
    && apt-get install -y --no-install-recommends \
        ffmpeg

RUN pip install pipenv
RUN pipenv lock -r > requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]