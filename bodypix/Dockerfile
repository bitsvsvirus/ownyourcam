FROM node:latest

WORKDIR /app
COPY . .
RUN yarn upgrade
RUN yarn

EXPOSE 1234
CMD ["yarn", "watch"]

