# Utilizza un'immagine Node.js per costruire l'app Vue.js
FROM node:14 AS build-stage

WORKDIR /app

# Copia i file del frontend
COPY . .

# Imposta la variabile d'ambiente per la URL del backend
ARG VUE_APP_BACKEND_URL
ENV VUE_APP_BACKEND_URL=${VUE_APP_BACKEND_URL}

# Installa le dipendenze e crea la build dell'app
RUN npm install && npm run build

# Nginx per servire i file statici
FROM nginx:latest AS production-stage

# Copia i file della build di Vue.js nella directory di Nginx
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copia il file di configurazione Nginx
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
