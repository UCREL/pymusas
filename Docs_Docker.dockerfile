FROM node:16.13-alpine3.15

RUN apk add --no-cache git

USER node

RUN mkdir /home/node/website

WORKDIR /home/node/website

EXPOSE 3000

ENTRYPOINT ["/bin/sh"]