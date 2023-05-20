FROM node:14

WORKDIR /usr/src/app
ENV PORT 8091
ENV TARGET_URL https://example.com
COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 8091

CMD [ "npm", "start" ]

