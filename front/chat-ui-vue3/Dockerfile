FROM node:20-slim

WORKDIR /app

COPY package.json package-lock.json ./

RUN NODE_ENV=development npm install

COPY . .

# Fix EACCES
ENV BABEL_CACHE_PATH=/tmp/.babel-cache
ENV ESLINT_CACHE_LOCATION=/tmp/.eslint-cache

EXPOSE 8080

CMD ["npx", "vue-cli-service", "serve", "--host", "0.0.0.0", "--port", "8080"]
