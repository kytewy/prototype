FROM node:20-bookworm

# Set the working directory
WORKDIR /app

# Install pnpm globally
RUN npm install -g pnpm

# Copy package files and install dependencies
COPY package*.json ./

# Install dependencies
RUN pnpm install

# Copy the rest of your application code
COPY . .

# Fix permissions for the .next directory
RUN mkdir -p /app/.next && chmod 777 /app/.next

EXPOSE 3000

# Start the application
CMD ["pnpm", "run", "dev"]