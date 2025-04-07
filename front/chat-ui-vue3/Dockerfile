FROM node:20-slim

WORKDIR /app

COPY package.json package-lock.json ./

ENV NODE_ENV=development

RUN npm install

COPY . .

# Fix EACCES
ENV BABEL_CACHE_PATH=/tmp/.babel-cache
ENV ESLINT_CACHE_LOCATION=/tmp/.eslint-cache

EXPOSE 8080

CMD ["npm", "run", "serve"]

