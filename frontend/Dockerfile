FROM node:10-alpine as build-stage 
RUN apk add git
WORKDIR /app 
COPY package*.json ./ 
COPY docker/build/nginx.conf /nginx.conf 
 
RUN npm install 
COPY . . 
RUN npm run build 
 
FROM nginx:1.13.12-alpine as production-stage 
COPY --from=build-stage /app/dist /usr/share/nginx/html 
COPY --from=build-stage /nginx.conf /etc/nginx/nginx.conf 
 
EXPOSE 80 
 
CMD ["nginx", "-g", "daemon off;"]