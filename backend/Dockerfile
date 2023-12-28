FROM ubuntu

# Copia i file nel container
COPY . /root/

# Imposta la directory di lavoro
WORKDIR /root/

# Installa python3-pip e le dipendenze del progetto
# e rendi eseguibile lo script di avvio
RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install --no-cache-dir -r requirements.txt && \
    chmod +x boot.sh

# Imposta lo script di avvio come entrypoint
ENTRYPOINT ["./boot.sh"]
