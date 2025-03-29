# Étape de build
FROM node:16-alpine as build

WORKDIR /app

# Copie des fichiers de configuration
COPY package.json .
COPY package-lock.json* .
COPY tsconfig.json .
COPY tsconfig.node.json .
COPY vite.config.ts .

# Installation des dépendances
RUN npm ci

# Copie du code source
COPY src/ src/
COPY public/ public/
COPY index.html .

# Construction de l'application
RUN npm run build

# Étape de production
FROM nginx:stable-alpine

# Copie du résultat de la construction
COPY --from=build /app/build /usr/share/nginx/html

# Copie de la configuration nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exposition du port
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
