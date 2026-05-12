FROM node:20-alpine AS builder

WORKDIR /app

ENV NODE_ENV=production
ENV CI=1
ENV EXPO_NO_TELEMETRY=1

COPY package.json ./
RUN npm install --legacy-peer-deps

COPY . .

ARG EXPO_PUBLIC_API_URL=http://213.32.18.160:8000
ENV EXPO_PUBLIC_API_URL=$EXPO_PUBLIC_API_URL

RUN npx expo export -p web

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

RUN echo 'server { \
    listen 80; \
    root /usr/share/nginx/html; \
    index index.html; \
    location / { \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
