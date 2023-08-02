# Use the official Nginx base image
FROM nginx

# Remove default Nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/

# Expose port 80 for Nginx
EXPOSE 80 443
