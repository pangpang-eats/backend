FROM python:3.9.5-buster

WORKDIR /usr/src/app

ENV PYTHONBUFFERED 1


# install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade pip;\
    pip install -r --no-cache-dir requirements.txt

# copy source code
COPY . .
RUN chmod +x migrate_and_execute.sh;\
    python manage.py collectstatic --noinput

CMD [ "sh", "migrate_and_execute.sh"]