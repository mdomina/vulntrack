#!/bin/bash

# Script per installare Python 3.10 su Ubuntu con supporto per zlib e SSL
# Esegui questo script con privilegi di superutente (sudo)

echo "Aggiornamento del sistema..."
if apt update; then
  echo "Aggiornamento del sistema completato con successo."
else
  echo "Errore durante l'aggiornamento del sistema." >&2
  exit 1
fi

echo "Installazione delle librerie necessarie per la compilazione..."
if apt install -y \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libgdbm-dev \
    libbz2-dev \
    libffi-dev \
    liblzma-dev \
    libnss3-dev \
    libexpat1-dev \
    tk-dev \
    openssl \
    wget \
    curl; then
  echo "Installazione delle librerie completata con successo."
else
  echo "Errore durante l'installazione delle librerie." >&2
  exit 1
fi

echo "Scaricamento di Python 3.10..."
cd /usr/src
if wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz; then
  echo "Scaricamento di Python 3.10 completato con successo."
else
  echo "Errore durante il download di Python 3.10." >&2
  exit 1
fi

echo "Estrazione dei sorgenti di Python 3.10..."
if tar xzf Python-3.10.0.tgz; then
  echo "Estrazione dei sorgenti completata con successo."
else
  echo "Errore durante l'estrazione dei sorgenti di Python 3.10." >&2
  exit 1
fi

echo "Configurazione di Python 3.10..."
cd Python-3.10.0
if ./configure --enable-optimizations --with-ssl; then
  echo "Configurazione di Python 3.10 completata con successo."
else
  echo "Errore durante la configurazione di Python 3.10." >&2
  exit 1
fi

echo "Compilazione di Python 3.10..."
if make -j$(nproc); then
  echo "Compilazione di Python 3.10 completata con successo."
else
  echo "Errore durante la compilazione di Python 3.10." >&2
  exit 1
fi

echo "Installazione di Python 3.10..."
if make altinstall; then
  echo "Installazione di Python 3.10 completata con successo."
else
  echo "Errore durante l'installazione di Python 3.10." >&2
  exit 1
fi

echo "Verifica dell'installazione di Python 3.10..."
if python3.10 --version; then
  echo "Python 3.10 installato correttamente."
else
  echo "Errore durante la verifica dell'installazione di Python 3.10." >&2
  exit 1
fi

echo "Verifica del supporto per zlib e ssl in Python 3.10..."
if python3.10 -c "import zlib; import ssl; print('zlib e ssl sono disponibili')"; then
  echo "Supporto per zlib e SSL verificato con successo."
else
  echo "Errore: Python 3.10 non ha supporto per zlib e SSL." >&2
  exit 1
fi

echo "Installazione completata con successo!"
