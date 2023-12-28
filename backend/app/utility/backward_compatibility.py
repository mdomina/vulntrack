# dopo il cambio del template del remediation plan è necessario conformare i 2 templates. Questo file serve per la retrocompabilità dei vecchi report.

def b_c(df):
    # livello di rischio / gravità 
    if 'livello di rischio' in df.columns:
        df = df.rename(columns={'livello di rischio': 'gravità'})

    if 'nome vulnerabilità' in df.columns:
        df = df.rename(columns={'nome vulnerabilità': 'vulnerabilità'})
    
    if 'tipologia' in df.columns:
        df = df.rename(columns={'tipologia': 'categoria'})
    
    if 'risorsa impattata' in df.columns:
        df = df.rename(columns={'risorsa impattata': 'risorsa'})
    
    if 'azioni di rimedio' in df.columns:
        df = df.rename(columns={'azioni di rimedio': 'contromisure'})
    return df