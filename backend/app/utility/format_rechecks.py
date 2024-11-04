def filter_rechecks(input_data: list[dict]):
    """
    Filtra e formatta i dati di audit per distinguere se ciascuna app per ciascun cliente
    è stata sottoposta a un controllo iniziale ('vapt') e/o a un recheck.

    Args:
        input_data (list[dict]): Lista di dizionari, ciascuno contenente informazioni sugli audit.
            Ogni dizionario rappresenta un audit con i seguenti campi chiave:
                - 'nome' (str): Nome dell'app.
                - 'cliente' (str): Nome del cliente associato all'app.
                - 'type' (str): Tipo di audit, può essere 'Recheck' o un altro tipo di audit.

    Returns:
        list[dict]: Una lista di dizionari, ciascuno rappresentante un'app per un cliente specifico,
        con i seguenti campi:
            - 'anno' (str): Anno dell'audit.
            - 'mese' (str): Mese dell'audit.
            - 'nome' (str): Nome dell'app.
            - 'vapt' (bool): Flag che indica se l'app è stata sottoposta a un controllo iniziale.
            - 'recheck' (bool): Flag che indica se l'app è stata sottoposta a un recheck.
            - 'codice_elettra' (str): Codice elettro per l'app (default '-').
            - 'cliente' (str): Nome del cliente associato all'app.

    Note:
        La funzione crea un dizionario 'seen' in cui ogni chiave è una tupla composta da
        ('nome', 'cliente'), per tenere traccia di ogni app specifica per ciascun cliente.
        In base al campo 'type' di ogni entry, i flag 'vapt' e 'recheck' vengono impostati
        rispettivamente su True se l'app è stata soggetta a un controllo iniziale e/o un recheck.

    Example:
        input_data = [
            {"nome": "App1", "cliente": "ClienteA", "type": "Initial"},
            {"nome": "App1", "cliente": "ClienteA", "type": "Recheck"},
            {"nome": "App1", "cliente": "ClienteB", "type": "Initial"}
        ]
        output = filter_rechecks(input_data)
        # output sarà una lista con flag 'vapt' e 'recheck' per ciascun cliente per 'App1'.
    """
    
    # Dizionario per tenere traccia delle app per ciascun cliente.
    seen = {}

    for entry in input_data:
        # Creiamo una chiave composta da "nome" e "cliente" per distinguere le app per cliente.
        key = (entry["nome"], entry["cliente"])

        # Se la coppia (nome, cliente) non è stata ancora vista, aggiungila al dizionario.
        if key not in seen:
            entry["vapt"] = False
            entry["recheck"] = False
            seen[key] = entry

        # Aggiorna i flag 'vapt' e 'recheck' in base al 'type' corrente.
        if entry["type"] == "Recheck":
            seen[key]["recheck"] = True
        elif entry["type"] != "Recheck":
            seen[key]["vapt"] = True

    # Rimuoviamo il campo 'type' e ritorniamo solo i valori del dizionario 'seen' come lista.
    for value in seen.values():
        del value["type"]

    return list(seen.values())



if __name__=='__main__':
    data = []

    output = filter_rechecks(data)
    print(output)
