FROM nginx:alpine

# Install curl to fetch the internal IP
RUN apk update && apk add curl

# Add our configuration template
COPY job_queue_service.conf /etc/nginx/conf.d/job_queue_service.template


# Copy the start-up script and make it executable
COPY start-nginx.sh /
RUN chmod +x /start-nginx.sh

CMD ["/start-nginx.sh"]