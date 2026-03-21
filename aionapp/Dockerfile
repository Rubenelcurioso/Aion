FROM node:18-alpine

WORKDIR /app

# Copy package.json and package-lock.json first for cache optimization
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy all files
COPY . .

# Expose port
EXPOSE 3000

# Start command
CMD ["npm", "run", "dev"]
