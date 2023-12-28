# VulnTrack: Sistema di Gestione Risultati VAPT

## Panoramica
VulnTrack è uno strumento specializzato progettato per gestire e tracciare i risultati dell'Analisi di Vulnerabilità e dei Test di Penetrazione (VAPT). È uno strumento essenziale per i professionisti della sicurezza informatica e le organizzazioni per tenere traccia delle vulnerabilità nei loro sistemi e garantire risoluzioni tempestive.

## Componenti
Il progetto VulnTrack è strutturato come segue:
- `backend`: Il componente server backend di VulnTrack.
- `frontend`: L'interfaccia utente per interagire con VulnTrack.
- `frontend_dev`: Ambiente di sviluppo per il frontend.
- `docker-compose.yml`: File Docker Compose per orchestrare l'ambiente di VulnTrack.

## Configurazione del Backend
Il backend di VulnTrack è collegato alla rete di PwnDoc. Se si desidera utilizzare VulnTrack in modo separato, è necessario disporre di un database MongoDB. Questo approccio fornisce flessibilità per gli utenti che desiderano utilizzare VulnTrack in diversi ambienti o configurazioni.

## Installazione e Avvio
Per avviare VulnTrack, assicurati di avere Docker e Docker Compose installati sul tuo sistema. Una volta installati, puoi avviare il progetto eseguendo il seguente comando nella directory principale:

```bash
docker-compose up
```

Questo comando costruirà e avvierà sia il backend che il frontend di VulnTrack, rendendoli accessibili attraverso i rispettivi endpoint.

## Contribuire
Contributi al progetto sono benvenuti. Se desideri contribuire, considera di fare un fork del progetto, apportare le tue modifiche e inviare una pull request.

## Licenza
VulnTrack è rilasciato sotto [inserire tipo di licenza qui], che permette l'utilizzo, la modifica e la distribuzione per diversi scopi.

---

Nota: Assicurati di includere dettagli specifici come requisiti di sistema, istruzioni di installazione dettagliate, informazioni sulla licenza effettiva e qualsiasi altra informazione rilevante per gli utenti e i contributori del tuo progetto.
