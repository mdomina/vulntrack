FROM python:3.10-slim

# Copia i file nel container
COPY . /root/

# Imposta la directory di lavoro
WORKDIR /root/

# Installa LibreOffice e dipendenze
RUN apt-get update && apt-get install -y \
    libreoffice \
    libreoffice-core \
    libreoffice-writer \
    && apt-get clean

# Installa le dipendenze nel virtual environment
RUN pip install -r requirements.txt

RUN chmod +x boot.sh

EXPOSE 80

# Imposta lo script di avvio come entrypoint
ENTRYPOINT ["./boot.sh"]
