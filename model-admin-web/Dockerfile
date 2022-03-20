FROM node:17.7.2 as builder

RUN npm install -g @angular/cli

ADD ./ /home/node
WORKDIR /home/node
RUN npm install
RUN ng build

FROM nginx:1.21.6

COPY --from=builder /home/node/dist/* /www/data/
COPY nginx.conf /etc/nginx


