FROM nginx:alpine

ARG CACHEBUST=1

COPY web-app.html /usr/share/nginx/html/index.html

RUN echo "voyager-v2-static" > /usr/share/nginx/html/version.txt

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
