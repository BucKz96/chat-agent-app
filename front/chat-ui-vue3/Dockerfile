FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 8080

CMD ["npx", "vue-cli-service", "serve", "--host", "0.0.0.0", "--port", "8080"]

