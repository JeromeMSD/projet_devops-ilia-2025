FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:1.27-alpine AS runtime

RUN addgroup -S app && adduser -S app -G app

COPY --from=builder /app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /var/cache/nginx /var/run/nginx \
    && chown -R app:app /usr/share/nginx/html /var/cache/nginx /var/run/nginx

USER app

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
