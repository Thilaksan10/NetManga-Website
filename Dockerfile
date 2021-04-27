FROM python:3.9-alpine

ENV PATH="/scripts:${PATH}"

COPY ./requirements/prod.txt /requirements/prod.txt
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN apk add python3-dev musl-dev postgresql-dev jpeg-dev zlib-dev libjpeg libpcre3 libpcre3-dev
RUN pip install -r /requirements/prod.txt
RUN apk del .tmp

RUN mkdir /netmanga_website
COPY ./netmanga_website /netmanga_website
WORKDIR /netmanga_website
COPY ./scripts /scripts

RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser -D user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web
USER user

CMD ["entrypoint.sh"]