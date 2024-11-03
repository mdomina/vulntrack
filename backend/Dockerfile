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
    
# Rende eseguibile lo script di installazione di Python 3.10
# RUN chmod +x install_python3.10.sh

# Esegue lo script per installare Python 3.10
# RUN ./install_python3.10.sh

# Crea un ambiente virtuale con Python 3.10
# RUN python3.10 -m venv venv

# Installa le dipendenze nel virtual environment
RUN pip install -r requirements.txt

RUN chmod +x boot.sh

# Imposta lo script di avvio come entrypoint
ENTRYPOINT ["./boot.sh"]
