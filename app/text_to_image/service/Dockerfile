FROM node:10

WORKDIR /var/www/app

COPY package*.json .

RUN npm i

COPY app.js .
COPY router.js .

EXPOSE 8080

ENTRYPOINT [ "npm", "start"]
