FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Run the dev server
CMD ["npm", "run", "dev", "--", "--host"]
