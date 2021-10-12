FROM node:14.18-alpine3.14

USER node

WORKDIR /home/node/website

EXPOSE 3000

ENTRYPOINT ["/bin/sh"]