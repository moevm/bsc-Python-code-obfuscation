FROM node:10

WORKDIR /var/www/app

COPY package*.json ./

RUN npm ci --only=production

COPY app.js .
COPY router.js .

EXPOSE 8080

ENTRYPOINT [ "npm", "start"]
