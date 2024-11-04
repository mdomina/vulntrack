# VulnTrack: Sistema di Gestione Risultati VAPT

## Panoramica
VulnTrack è uno strumento specializzato progettato per gestire e tracciare i risultati dell'Analisi di Vulnerabilità e dei Test di Penetrazione (VAPT). È uno strumento essenziale per i professionisti della sicurezza informatica e le organizzazioni, utile per tenere traccia delle vulnerabilità nei loro sistemi e garantire risoluzioni tempestive.

## Componenti
Il progetto VulnTrack è strutturato come segue:
- `backend`: Il componente server backend di VulnTrack.
- `frontend`: L'interfaccia utente per interagire con VulnTrack.
- `docker-compose.yml`: File Docker Compose per orchestrare l'ambiente di VulnTrack.
- `install_docker.sh`: Script per installare Docker Engine e Docker Compose (se non sono già presenti sul server).

## Configurazione del Backend
Il backend di VulnTrack richiede una connessione a un'istanza di MongoDB. Non è possibile utilizzare VulnTrack in modo separato dalla rete di PwnDoc, assicurarsi che il database MongoDB sia accessibile e configurato correttamente. Questo approccio fornisce flessibilità per gli utenti che desiderano utilizzare VulnTrack in diversi ambienti o configurazioni.

## Configurazione del Frontend
Nel frontend, le richieste API sono indirizzate al backend tramite la variabile `VUE_APP_BACKEND_URL`, impostata come argomento di build Docker, lasciando **/api** come endpoint per il reverse proxy. Durante la configurazione, puoi specificare l'URL del backend, come mostrato di seguito nel `docker-compose.yml`:

```yaml
vulntrack_frontend:
  build:
    context: ./frontend/
    args:
      VUE_APP_BACKEND_URL: "https://ip-backend/api"  # Imposta l'URL del backend 
  image: vulntrack/frontend:1.0
  container_name: vulntrack_frontend
  restart: always
```

## Installazione e Avvio

1. **Installazione di Docker**  
   Se Docker e Docker Compose non sono installati sul server, esegui lo script `install_docker.sh` presente nella directory principale del progetto. Questo script installerà le versioni necessarie di Docker e Docker Compose.

   ```bash
   chmod +x install_docker.sh
   ./install_docker.sh
   ```

2. **Avviare VulnTrack**  
   Una volta che Docker è installato, esegui il seguente comando nella directory principale per costruire e avviare VulnTrack:

   ```bash
   docker-compose up --build
   ```

   Questo comando costruirà e avvierà sia il backend che il frontend di VulnTrack, rendendoli accessibili attraverso i rispettivi endpoint.

3. **Accesso all'Applicazione**  
   Dopo aver eseguito `docker-compose up`, l'applicazione sarà accessibile tramite i seguenti endpoint:
   - **Frontend**: di default alla porta `80` se stai usando un container `nginx_proxy` per gestire la rete.
   - **Backend**: configurato in base alle impostazioni `MONGODB_HOST` e `MONGODB_PORT` in `docker-compose.yml`.

## Variabili di Configurazione

### Frontend
- `VUE_APP_BACKEND_URL`: Indirizzo base del backend a cui il frontend invierà le richieste API. Viene configurato tramite `docker-compose.yml` e utilizzato in `main.js` per impostare `axios.defaults.baseURL`.

### Backend
- `MONGODB_HOST`: Indirizzo IP o hostname del database MongoDB. Impostato nel `docker-compose.yml` con:
  
  \```yaml
  environment:
    - MONGODB_HOST=
  \```

- `MONGODB_PORT`: Porta utilizzata per il collegamento al database MongoDB. Impostato nel `docker-compose.yml` con:
  
  \```yaml
  environment:
    - MONGODB_PORT=
  \```

- `PWNDOC_HOST`: Indirizzo IP o hostname di PwnDoc per l'integrazione, impostato nel `docker-compose.yml` con:
  
  \```yaml
  environment:
    - PWNDOC_HOST=
  \```

- `PWNDOC_PORT`: Porta utilizzata per il collegamento a PwnDoc, impostata nel `docker-compose.yml` con:
  
  \```yaml
  environment:
    - PWNDOC_PORT=
  \```

## Contribuire
Contributi al progetto sono benvenuti. Se desideri contribuire, fai un fork del progetto, apporta le tue modifiche e invia una pull request.

## Licenza
VulnTrack è rilasciato sotto [inserire tipo di licenza qui], che permette l'utilizzo, la modifica e la distribuzione per diversi scopi.

---
