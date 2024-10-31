FROM ubuntu:24.04

# Copia i file nel container
COPY . /root/

# Imposta la directory di lavoro
WORKDIR /root/

# Installa python3-pip e le dipendenze del progetto
# e rendi eseguibile lo script di avvio
RUN chmod +x install_python3.10.sh && \
    ./install_python3.10.sh && \
    python3.10 -m venv venv && \
    ./venv/bin/pip install -r requirements.txt && \
    chmod +x boot.sh
RUN ls /root
# Imposta lo script di avvio come entrypoint
ENTRYPOINT ["./boot.sh"]
