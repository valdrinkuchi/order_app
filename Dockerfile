FROM python:3.8-alpine

ENV PATH="/scripts:${PATH}"

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers python3-dev musl-dev zlib-dev jpeg-dev
RUN apk add --update --no-cache postgresql-dev
RUN pip install psycopg2-binary
RUN pip install -r /requirements.txt
RUN apk del .tmp

RUN mkdir /app
COPY . /app
WORKDIR /app
COPY ./scripts /scripts
RUN apk --update add bash && \
    apk add dos2unix

# RUN dos2unix /scripts/entrypoint.sh

RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/

RUN adduser -D user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web
USER user

CMD ["entrypoint.sh"]