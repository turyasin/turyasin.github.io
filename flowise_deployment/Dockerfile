FROM node:18-alpine

WORKDIR /app

# Install Flowise
RUN npm install -g flowise@2.0.0

# Expose port
EXPOSE 8080

# Start Flowise
CMD ["flowise", "start"]
