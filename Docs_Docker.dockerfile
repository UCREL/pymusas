FROM node:16.13.0-alpine3.14

RUN apk add --no-cache git

USER node

WORKDIR /home/node/website

EXPOSE 3000

ENTRYPOINT ["/bin/sh"]