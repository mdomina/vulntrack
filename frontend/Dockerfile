# Usa l'immagine Nginx di base
FROM nginx:latest

# Crea la directory di destinazione se non esiste
RUN mkdir -p /var/www/html

# Copia i contenuti dell'app nella directory di Nginx
COPY ./dist /var/www/html/

# Copia la configurazione di Nginx personalizzata
COPY nginx.conf /etc/nginx/nginx.conf

# Espone solo la porta 80 per HTTP
EXPOSE 80
