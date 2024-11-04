#!/bin/bash

echo "Aggiornamento dei pacchetti..."
if apt-get update; then
  echo "Aggiornamento dei pacchetti completato con successo."
else
  echo "Errore durante l'aggiornamento dei pacchetti." >&2
  exit 1
fi

echo "Installazione di ca-certificates e curl..."
if apt-get install -y ca-certificates curl; then
  echo "Installazione di ca-certificates e curl completata con successo."
else
  echo "Errore durante l'installazione di ca-certificates e curl." >&2
  exit 1
fi

echo "Creazione della directory /etc/apt/keyrings..."
if install -m 0755 -d /etc/apt/keyrings; then
  echo "Directory creata con successo."
else
  echo "Errore durante la creazione della directory." >&2
  exit 1
fi

echo "Scaricamento della chiave GPG ufficiale di Docker..."
if curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc; then
  echo "Chiave GPG scaricata con successo."
else
  echo "Errore durante il download della chiave GPG." >&2
  exit 1
fi

echo "Impostazione dei permessi per la chiave GPG..."
if chmod a+r /etc/apt/keyrings/docker.asc; then
  echo "Permessi impostati correttamente."
else
  echo "Errore nell'impostazione dei permessi per la chiave GPG." >&2
  exit 1
fi

echo "Aggiunta del repository Docker alle sorgenti di Apt..."
if echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null; then
  echo "Repository Docker aggiunto con successo."
else
  echo "Errore durante l'aggiunta del repository Docker." >&2
  exit 1
fi

echo "Aggiornamento dell'indice dei pacchetti..."
if apt-get update; then
  echo "Aggiornamento dell'indice dei pacchetti completato con successo."
else
  echo "Errore durante l'aggiornamento dell'indice dei pacchetti." >&2
  exit 1
fi

echo "Installazione dei pacchetti Docker..."
if apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin; then
  echo "Installazione dei pacchetti Docker completata con successo."
else
  echo "Errore durante l'installazione dei pacchetti Docker." >&2
  exit 1
fi

echo "Installazione completata con successo!"
