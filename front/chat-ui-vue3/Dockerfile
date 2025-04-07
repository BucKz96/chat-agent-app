FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

# Fix EACCES
ENV BABEL_CACHE_PATH=/tmp/.babel-cache
ENV ESLINT_CACHE_LOCATION=/tmp/.eslint-cache

EXPOSE 8080

# use npx for vue-cli-service unfound
CMD ["npx", "vue-cli-service", "serve", "--host", "0.0.0.0", "--port", "8080"]