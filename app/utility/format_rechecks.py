def filter_rechecks(input_data):
    # Dizionario per tenere traccia dei 'nomi' che sono già stati visti.
    seen = {}

    for entry in input_data:
        key = entry["nome"]

        # Se il 'nome' corrente non è stato ancora visto, aggiungilo al dizionario.
        if key not in seen:
            entry["vapt"] = False
            entry["recheck"] = False
            seen[key] = entry

        # Aggiorna i flag 'vapt' e 'recheck' in base al 'type' corrente.
        if entry["type"] == "recheck":
            seen[key]["recheck"] = True
        elif entry["type"] == "vapt":
            seen[key]["vapt"] = True

    # Ora che abbiamo processato tutti i dati, rimuoviamo il campo 'type' e ritorniamo solo i valori del dizionario 'seen' come lista.
    for value in seen.values():
        del value["type"]

    return list(seen.values())


if __name__=='__main__':
    data = []

    output = filter_rechecks(data)
    print(output)
