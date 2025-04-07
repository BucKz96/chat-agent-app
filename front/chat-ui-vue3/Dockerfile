FROM node:20-alpine

RUN npm install -g @vue/cli@5

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install

COPY . .

# Fix EACCES
ENV BABEL_CACHE_PATH=/tmp/.babel-cache
ENV ESLINT_CACHE_LOCATION=/tmp/.eslint-cache

EXPOSE 8080

CMD ["sh", "-c", "vue-cli-service serve --host 0.0.0.0 --port 8080"]