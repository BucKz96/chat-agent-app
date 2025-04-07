FROM node:20-alpine

# 1. Install vue-cli-service globally
RUN npm install -g @vue/cli-service@5.0.10

# 2. Prepare app folder
WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 8080

CMD ["vue-cli-service", "serve", "--host", "0.0.0.0", "--port", "8080"]
