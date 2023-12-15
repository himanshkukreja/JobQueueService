#!/bin/sh

# Fetch the internal IP
INTERNAL_IP=$(curl -s http://169.254.169.254/latest/meta-data/local-ipv4)
echo "Fetched Internal IP: $INTERNAL_IP"


# Replace the placeholder in the configuration with the actual internal IP

sed "s/\${INTERNAL_IP}/$INTERNAL_IP/g" /etc/nginx/conf.d/job_queue_service.template > /etc/nginx/conf.d/default.conf

# Start nginx
nginx -g 'daemon off;'