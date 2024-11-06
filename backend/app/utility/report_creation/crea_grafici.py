from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import os
import numpy as np
import textwrap

class Dashboard:
    """classe per creare grafici dalla pagina web dashboard generale"""
    def __init__(self, base_dir=None):
        """
        Costruttore per Dashboard che configura le directory.
        
        :param base_dir: Directory di base in cui vengono salvati i grafici. 
                         Se None, viene utilizzata la directory corrente.
        """
        # Imposta la directory di base per i grafici
        self.base_dir = base_dir if base_dir else os.path.dirname(__file__)
        self.graph_dir = os.path.join(self.base_dir, 'grafici')
        # Mappa dei colori per le severità
        self.severity_color_map = {
            'Critical': 'brown',
            'High': 'red',
            'Medium': 'orange',
            'Low': 'green'
        }

        # Crea la directory per i grafici se non esiste
        if not os.path.exists(self.graph_dir):
            os.makedirs(self.graph_dir)

    @staticmethod
    def insert_line_break_after_third_space(text):
        """
        Inserisce un 'a capo' ('\n') dopo il terzo spazio in una stringa, se ci sono almeno tre spazi.
        """
        words = text.split(' ')
        if len(words) > 3:
            return ' '.join(words[:3]) + '\n' + ' '.join(words[3:])
        else:
            return text
  
    def create_radar_chart_by_category(self, labels, sizes, output_filename):
        """
        Crea un grafico radar per visualizzare i dati di vulnerabilità per categorie, 
        assicurando che ci siano almeno 5 categorie per una migliore leggibilità.

        Se i dati originali contengono meno di 5 categorie, vengono aggiunte categorie fisse 
        con valore 0 fino a raggiungere il numero minimo di categorie. Le categorie fisse sono:
        'Injection', 'Security Misconfiguration', 'Insecure Design', 'Broken Access Control', 
        'Cryptographic Failures'.

        :param labels: Lista delle categorie di vulnerabilità (etichette).
        :param sizes: Lista dei valori associati a ciascuna categoria.
        :param output_filename: Nome del file per salvare il grafico generato.
        """

        # Definisce le categorie fisse per garantire un minimo di 5 categorie
        fixed_categories = ['Injection', 'Security Misconfiguration', 'Insecure Design', 
                            'Broken Access Control', 'Cryptographic Failures']

        # Crea un dizionario delle categorie e conteggi
        data_dict = dict(zip(labels, sizes))

        # Aggiunge le categorie fisse mancanti con valore 0 per garantire almeno 5 categorie
        for category in fixed_categories:
            if category not in data_dict:
                data_dict[category] = 0

        # Aggiorna labels e sizes con le categorie e i valori definitivi
        labels = list(data_dict.keys())
        sizes = list(data_dict.values())

        # Applica la funzione `insert_line_break_after_third_space` a ciascuna etichetta
        labels = [self.insert_line_break_after_third_space(label) for label in labels]

        # Calcola il numero di categorie aggiornato
        num_vars = len(labels)

        # Calcola gli angoli per ciascuna categoria in modo circolare
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

        # Completa il ciclo per chiudere il radar
        sizes += sizes[:1]
        angles += angles[:1]

        # Inizializza il grafico radar
        fig, ax = plt.subplots(subplot_kw=dict(polar=True))

        # Traccia i dati e riempie l'area sottostante
        ax.plot(angles, sizes, color='skyblue', linewidth=2, linestyle='solid')
        ax.fill(angles, sizes, color='skyblue', alpha=0.4)

        # Imposta le etichette delle categorie con i nuovi titoli multilinea
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, ha='center', fontsize=10, color='black')

        # Sposta le etichette fuori dal grafico
        ax.xaxis.set_tick_params(pad=20)

        # Rimuove le etichette radiali
        ax.set_yticklabels([])

        # Aggiunge i valori di ogni categoria
        for angle, size in zip(angles, sizes):
            ax.text(angle, size + 0.1, f"{size}", ha='center', va='center', fontsize=10, color='black')

        # Salva il grafico come file
        file = os.path.join(self.graph_dir, output_filename)
        plt.savefig(file)
        plt.close()

    def horizontal_bar_chart_by_name(self, labels, sizes, output_filename):
        """
        Crea un grafico a barre orizzontali per visualizzare i dati basati su nomi specifici.

        Questa funzione genera un grafico a barre orizzontali, con ciascuna barra che rappresenta
        il numero associato a una specifica etichetta. Il grafico è salvato come file immagine
        nella directory specificata.

        :param labels: Lista di etichette per ciascuna barra del grafico.
        :param sizes: Lista di valori numerici che determinano la lunghezza di ciascuna barra.
        :param output_filename: Nome del file in cui salvare il grafico generato.
        """
        
        # Determina il numero di etichette e calcola l'altezza della figura se i nomi delle vulnerabilità sono magiorni di 
        if len(labels) > 15:
            fig_height = max(1, len(labels) * 0.2)  # Imposta l'altezza in base al numero di etichette
        else:
            fig_height = 8
            
        # Crea una figura con altezza dinamica e larghezza fissa
        fig, ax = plt.subplots(figsize=(11, fig_height))

        # Disegna le barre orizzontali usando le etichette e le dimensioni fornite
        ax.barh(labels, sizes, color='skyblue', height=0.5)

        # Configura la dimensione dei tick delle etichette sull'asse y per migliorare la leggibilità
        ax.tick_params(axis='y', labelsize=10)

        # imposta il margine verticale tra il bordo e le barre se  i nomi delle vulnerabilità sono maggiori di 
        if len(labels) > 10:
            ax.margins(y=0.01) 
        
        # Applica un layout compatto per ridurre gli spazi bianchi
        plt.tight_layout()

        # Salva il grafico come immagine nel percorso specificato
        file = os.path.join(self.graph_dir, output_filename)
        plt.savefig(file)
        plt.close()  # Chiude la figura per liberare memoria

    def total_vuln_pie_chart(self, labels, sizes, colors, output_filename):
        """
        Crea un grafico a torta con spazi tra le sezioni per rappresentare i dati.

        Questa funzione genera un grafico a torta basato sulle etichette, dimensioni e colori forniti.
        Le sezioni del grafico sono distanziate per migliorare la leggibilità. Gli elementi con size=0
        vengono filtrati per evitare sezioni non visibili.

        :param labels: Lista di etichette per ciascuna sezione del grafico.
        :param sizes: Lista di dimensioni per ciascuna sezione del grafico.
        :param colors: Lista di colori per ciascuna sezione del grafico.
        :param output_filename: Nome del file in cui salvare il grafico generato.
        """
        
        # Filtra le etichette e le dimensioni per rimuovere gli elementi con size = 0
        # Questo evita di avere sezioni vuote nel grafico
        filtered_labels = [label for label, size in zip(labels, sizes) if size > 0]
        filtered_sizes = [size for size in sizes if size > 0]
        filtered_colors = [color for color, size in zip(colors, sizes) if size > 0]
        
        # Crea la lista explode per aggiungere spazio tra le sezioni
        # Ogni elemento nella lista rappresenta lo "spostamento" di una sezione dal centro del grafico
        # 0.1 significa che ogni sezione viene spostata leggermente per creare spazio
        explode = [0.01] * len(filtered_sizes)

        # Crea una nuova figura e un asse per il grafico a torta
        fig, ax = plt.subplots()

        # Funzione personalizzata per mostrare le percentuali solo per le sezioni con valore > 0
        # Se una percentuale è 0, non viene mostrata sul grafico
        def autopct_format(pct):
            return ('%1.1f%%' % pct) if pct > 0 else ''

        # Crea il grafico a torta
        ax.pie(
            filtered_sizes,                # Utilizza solo le dimensioni filtrate
            labels=filtered_labels,         # Utilizza solo le etichette filtrate
            autopct=autopct_format,         # Usa la funzione personalizzata per le percentuali
            startangle=90,                  # Avvia il grafico a torta a 90 gradi (in alto)
            colors=filtered_colors,         # Usa solo i colori filtrati
            explode=explode                 # Crea spazio tra le sezioni
        )
        ax.axis('equal')  # Imposta l'asse per mantenere il grafico come un cerchio perfetto

        # Salva il grafico come immagine nel percorso specificato
        file = os.path.join(self.graph_dir, output_filename)
        plt.savefig(file)
        plt.close()  # Chiudi la figura per liberare memoria

    def total_vuln_donut_chart(self, labels, sizes, output_filename):
        """
        Crea un grafico a ciambella (donut chart) con spazi tra le sezioni per rappresentare i dati.

        Questa funzione genera un grafico a ciambella basato sulle etichette, dimensioni e colori forniti.
        Le sezioni del grafico sono distanziate per migliorare la leggibilità. Gli elementi con size=0
        vengono filtrati per evitare sezioni non visibili.

        :param labels: Lista di etichette per ciascuna sezione del grafico.
        :param sizes: Lista di dimensioni per ciascuna sezione del grafico.
        :param colors: Lista di colori per ciascuna sezione del grafico.
        :param output_filename: Nome del file in cui salvare il grafico generato.
        """
        colors = ['brown', 'red', 'orange', 'green']  # I colori per ciascuna severità
        
        # Filtra le etichette e le dimensioni per rimuovere gli elementi con size = 0
        filtered_labels = [label for label, size in zip(labels, sizes) if size > 0]
        filtered_sizes = [size for size in sizes if size > 0]
        filtered_colors = [color for color, size in zip(colors, sizes) if size > 0]
        
        # Crea la lista explode per aggiungere spazio tra le sezioni
        explode = [0.01] * len(filtered_sizes)

        # Crea una nuova figura e un asse per il grafico a ciambella
        fig, ax = plt.subplots()

        # Funzione personalizzata per mostrare le percentuali solo per le sezioni con valore > 0
        def autopct_format(pct):
            return ('%1.1f%%' % pct) if pct > 0 else ''

        # Crea il grafico a ciambella
        wedges, texts, autotexts = ax.pie(
            filtered_sizes,
            labels=filtered_labels,
            autopct=autopct_format,
            startangle=90,
            colors=filtered_colors,
            explode=explode
        )
        
        # Aggiungi il "foro" per trasformare il grafico in una ciambella
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')  # Aggiunge un cerchio bianco al centro
        fig.gca().add_artist(centre_circle)  # Aggiunge il cerchio all'asse corrente

        ax.axis('equal')  # Imposta l'asse per mantenere il grafico come un cerchio perfetto

        # Salva il grafico come immagine nel percorso specificato
        file = os.path.join(self.graph_dir, output_filename)
        plt.savefig(file)
        plt.close()  # Chiudi la figura per liberare memoria

    def vuln_charts_by_vulnType(self, data, output_dir):
        """
        Crea e salva un grafico a barre per ciascuna categoria di vulnerabilità (vulnType),
        con le vulnerabilità suddivise per severità e con colori specifici per ciascuna severità.
        Mostra il totale delle vulnerabilità sopra ogni colonna e i numeri per ogni severità all'interno delle colonne.
        Ritorna una lista dei percorsi dei grafici salvati.
        
        :param data: Lista di dizionari contenente le informazioni sulle vulnerabilità.
        :param output_dir: Directory in cui salvare i grafici.
        :return: Lista dei percorsi dei file dei grafici salvati.
        """
        

        # Raggruppa le vulnerabilità per tipo (vulnType) e conta per severità
        vuln_by_type = defaultdict(lambda: defaultdict(Counter))
        saved_charts = []  # Lista per salvare i percorsi dei grafici

        # Popola il dizionario con il conteggio delle vulnerabilità per tipo e severità
        for entry in data:
            for finding in entry['findings']:
                vuln_type = finding['vulnType']
                vuln_title = finding['title']
                severity = finding['severity']
                vuln_by_type[vuln_type][vuln_title][severity] += 1

        # Crea e salva un grafico per ogni tipo di vulnerabilità
        for vuln_type, findings in vuln_by_type.items():
            titles = list(findings.keys())
            severity_counts = {severity: [] for severity in self.severity_color_map.keys()}

            # Suddividi i titoli in modo che siano multilinea solo dopo il terzo spazio
            wrapped_titles = [self.insert_line_break_after_third_space(title) for title in titles]

            # Costruisci i dati per ogni severità
            for title in titles:
                for severity in self.severity_color_map.keys():
                    severity_counts[severity].append(findings[title].get(severity, 0))

            # Configura il grafico a barre per il tipo di vulnerabilità corrente
            fig, ax = plt.subplots(figsize=(10, 6))

            # Sovrapponi le barre per ogni severità
            bottom = [0] * len(titles)  # Per tracciare la base di ciascuna barra
            for severity, counts in severity_counts.items():
                bars = ax.bar(titles, counts, bottom=bottom, color=self.severity_color_map[severity], label=severity)
                
                # Aggiungi il numero per ciascuna sezione di severità
                for bar, count in zip(bars, counts):
                    if count > 0:  # Mostra solo se il conteggio è maggiore di 0
                        ax.text(
                            bar.get_x() + bar.get_width() / 2,  # Posiziona al centro della sezione
                            bar.get_y() + bar.get_height() / 2,  # Posiziona al centro dell'altezza della sezione
                            str(count), 
                            ha='center', 
                            va='center',
                            fontsize=8, 
                            color='white' if severity == 'Critical' or severity == 'High' else 'black'  # Testo bianco per sezioni scure
                        )
                # Aggiorna il fondo per la prossima severità
                bottom = [i + j for i, j in zip(bottom, counts)]

            # Aggiungi etichette e titolo
            ax.set_title(f"Conteggio delle Vulnerabilità per: {vuln_type}")
            
            # Imposta le posizioni dei tick dell'asse X in base al numero di titoli
            ax.set_xticks(range(len(wrapped_titles)))  # Aggiunge i tick in base al numero di titoli

            # Ruota le etichette dell'asse X per una migliore leggibilità
            ax.set_xticklabels(wrapped_titles, rotation=45, ha="right")

            
            # Imposta un limite superiore per l'asse y per aggiungere padding sopra le barre
            max_count = max([sum(count) for count in zip(*severity_counts.values())])
            ax.set_ylim(0, max_count * 1.15)  # Aggiunge un 15% di spazio sopra la barra più alta

            # Aggiungi la legenda per indicare i colori delle severità
            ax.legend(title="Severity", loc="upper right")

            # Calcola e aggiungi il totale sopra ciascuna colonna
            for i, title in enumerate(titles):
                total = sum(severity_counts[severity][i] for severity in self.severity_color_map.keys())
                ax.text(i, bottom[i], str(total), ha='center', va='bottom', fontsize=10)

            # Salva il grafico come immagine PNG
            chart_filename = f"{vuln_type.replace(' ', '_').lower()}_chart.png"
            chart_path = os.path.join(output_dir, chart_filename)
            plt.tight_layout()  # Assicura che tutto il contenuto sia all'interno del grafico
            plt.savefig(chart_path)
            plt.close()  # Chiudi il grafico per liberare memoria

            # Aggiungi il percorso del grafico salvato alla lista
            saved_charts.append(chart_path)

        # Ritorna la lista dei percorsi dei grafici salvati
        return saved_charts

    def create_bar_chart_by_category(self, labels, sizes, output_filename):
        fig, ax = plt.subplots()
        ax.bar(labels, sizes, color='skyblue', width=0.2)
        ax.set_xlim(-0.5, len(labels) - 0.5)
        # ax.set_ylabel('Numero di Vulnerabilità')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        file = os.path.join(self.graph_dir, output_filename)
        plt.savefig(file)
        plt.close()
 
    def create_horizontal_bar_chart_months(self, categories, critical, high, medium, low, output_filename):
        fig, ax = plt.subplots(figsize=(8, 6))  # Modifica le dimensioni della figura per adattare la legenda in basso
        bar_height = 0.3  # Imposta uno spessore delle barre più piccolo

        # Creazione delle barre
        ax.barh(categories, critical, label='Critical', color='brown', height=bar_height)
        ax.barh(categories, high, left=critical, label='High', color='red', height=bar_height)
        ax.barh(categories, medium, left=[i + j for i, j in zip(critical, high)], label='Medium', color='orange', height=bar_height)
        ax.barh(categories, low, left=[i + j + k for i, j, k in zip(critical, high, medium)], label='Low', color='green', height=bar_height)

        # Aggiungi i valori sulle barre
        for i, (crit, high_val, med, low_val) in enumerate(zip(critical, high, medium, low)):
            # Valore critico
            ax.text(crit / 2, i, str(crit), va='center', ha='center', color='white', fontsize=8)
            # Valore alto
            ax.text(crit + high_val / 2, i, str(high_val), va='center', ha='center', color='white', fontsize=8)
            # Valore medio
            ax.text(crit + high_val + med / 2, i, str(med), va='center', ha='center', color='white', fontsize=8)
            # Valore basso
            ax.text(crit + high_val + med + low_val / 2, i, str(low_val), va='center', ha='center', color='white', fontsize=8)

        # Aggiungi la legenda in basso
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4)  # Posiziona la legenda sotto il grafico
        
        # Aggiungi margini laterali per centrare meglio il grafico
        ax.margins(x=0.2)  # Aggiunge margini laterali sul lato x
        
        # Salva il grafico
        file = os.path.join(self.graph_dir, output_filename)
        plt.savefig(file, bbox_inches='tight')
        plt.close()

    def create_donut_chart(self, value, label, color, output_filename):
        fig, ax = plt.subplots()
        total = value if value > 0 else 1
        remainder = total - value
        ax.pie([value, remainder], labels=[label, ''], startangle=90, colors=[color, 'lightgrey'], 
               wedgeprops={'width': 0.3, 'edgecolor': 'white'}, 
               textprops={'fontsize': 20, 'color': 'black'})
        ax.text(0, 0, str(value), ha='center', va='center', fontsize=24, color=color)
        ax.axis('equal')
        file = os.path.join(self.graph_dir, output_filename)
        plt.savefig(file, transparent=True)
        plt.close()

    def create_all_donut_charts(self, data):
        for value, label, color, filename in data:
            self.create_donut_chart(value, label, color, filename)

    def create_bar_chart(self, categories, critical, high, medium, low, output_filename):
        fig, ax = plt.subplots()
        ax.bar(categories, critical, label='Critica', color='red', bottom=[high[j] + medium[j] + low[j] for j in range(len(categories))])
        ax.bar(categories, high, label='Alta', color='orange', bottom=[medium[j] + low[j] for j in range(len(categories))])
        ax.bar(categories, medium, label='Media', color='yellow', bottom=low)
        ax.bar(categories, low, label='Bassa', color='green')
        # ax.set_ylabel('Numero di Vulnerabilità')
        ax.legend()
        file = os.path.join(self.graph_dir, output_filename)
        plt.savefig(file)
        plt.close()


class Recheck:
    """classe per creare grafici per la pagina web del confronto tra vap e recheck"""
    def __init__(self, base_dir=None):
        """
        Costruttore per la classe Recheck che configura la directory per il salvataggio dei grafici.
        
        :param base_dir: Directory di base per i grafici; se None, viene utilizzata la directory corrente.
        """
        self.base_dir = base_dir if base_dir else os.path.dirname(__file__)
        self.graph_dir = os.path.join(self.base_dir, 'grafici')

        # Crea la directory per i grafici se non esiste
        if not os.path.exists(self.graph_dir):
            os.makedirs(self.graph_dir)

    def create_recheck_summary(self, data_vapt, data_recheck, output_filename):
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))
        categories = ['Critiche', 'Alte', 'Medie', 'Basse']
        colors = ['brown', 'red', 'orange', 'green']
        y_positions = [0.8, 0.55, 0.3, 0.05]

        # VAPT Summary
        for i, (value, category, color) in enumerate(zip(data_vapt, categories, colors)):
            axs[0].text(0.5, y_positions[i], f'{value}\n{category}', color='white',
                        ha='center', va='center', fontsize=16, fontweight='bold',
                        bbox=dict(facecolor=color, edgecolor=color, boxstyle='round,pad=0.6'))
        axs[0].axis('off')
        axs[0].set_title('VAPT', fontsize=16, fontweight='bold', y=1.05)

        # Recheck Summary
        for i, (value, category, color) in enumerate(zip(data_recheck, categories, colors)):
            axs[1].text(0.5, y_positions[i], f'{value}\n{category}', color='white',
                        ha='center', va='center', fontsize=16, fontweight='bold',
                        bbox=dict(facecolor=color, edgecolor=color, boxstyle='round,pad=0.6'))
        axs[1].axis('off')
        axs[1].set_title('Recheck', fontsize=16, fontweight='bold', y=1.05)

        # Salvataggio del file
        file = os.path.join(self.graph_dir, output_filename)
        plt.savefig(file, bbox_inches='tight')
        plt.close()

    def create_vapt_recheck_summary(self, data_vapt, data_recheck, output_filename):
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))
        categories = ['Critica', 'Alta', 'Media', 'Bassa']
        colors = ['brown', 'red', 'orange', 'green']

        # VAPT Summary
        for i, (value, category, color) in enumerate(zip(data_vapt, categories, colors)):
            axs[0].barh(category, value, color=color)
            axs[0].text(value, i, f'{value}', color='white', va='center', fontsize=12, fontweight='bold')
        axs[0].set_xlim(0, max(data_vapt) + 1)
        axs[0].set_title('VAPT', fontsize=16, fontweight='bold')

        # Recheck Summary
        for i, (value, category, color) in enumerate(zip(data_recheck, categories, colors)):
            axs[1].barh(category, value, color=color)
            axs[1].text(value, i, f'{value}', color='white', va='center', fontsize=12, fontweight='bold')
        axs[1].set_xlim(0, max(data_recheck) + 1)
        axs[1].set_title('Recheck', fontsize=16, fontweight='bold')

        file = os.path.join(self.graph_dir, output_filename)
        plt.savefig(file, bbox_inches='tight')
        plt.close()

    def create_vapt_recheck_histogram(self, data_vapt, data_recheck, categories, output_filename):
        fig, axs = plt.subplots(2, 1, figsize=(10, 10))

        # VAPT Histogram
        axs[0].barh(categories, data_vapt, color='skyblue')
        axs[0].set_title('VAPT', fontsize=16, fontweight='bold')
        #axs[0].set_xlabel('Numero di Vulnerabilità')
        #axs[0].set_ylabel('Tipologia')
        axs[0].invert_yaxis()

        # Recheck Histogram
        axs[1].barh(categories, data_recheck, color='skyblue')
        axs[1].set_title('Recheck', fontsize=16, fontweight='bold')
        # axs[1].set_xlabel('Numero di Vulnerabilità')
        # axs[1].set_ylabel('Tipologia')
        axs[1].invert_yaxis()

        file = os.path.join(self.graph_dir, output_filename)
        plt.savefig(file, bbox_inches='tight')
        plt.close()

    def create_histogram_vuln_by_name(self, labels_vapt, sizes_vapt, labels_recheck, sizes_recheck, output_file):
        fig, axs = plt.subplots(2, 1, figsize=(16, 18), sharex=True)
        fontsize = 10

        # VAPT Vulnerability Histogram
        axs[0].barh(labels_vapt, sizes_vapt, color='skyblue')
        axs[0].set_title('VAPT', fontsize=16, fontweight='bold')
        # 
        # xs[0].set_ylabel('Nome della Vulnerabilità', fontsize=fontsize)
        # axs[0].tick_params(axis='y', labelsize=fontsize)

        # Recheck Vulnerability Histogram
        axs[1].barh(labels_recheck, sizes_recheck, color='skyblue')
        axs[1].set_title('Recheck', fontsize=16, fontweight='bold')
        # axs[1].set_xlabel('Numero di Vulnerabilità', fontsize=fontsize)
        # axs[1].set_ylabel('Nome della Vulnerabilità', fontsize=fontsize)
        # axs[1].tick_params(axis='y', labelsize=fontsize)

        plt.subplots_adjust(left=0.3)
        file = os.path.join(self.graph_dir, output_file)
        plt.tight_layout()
        plt.savefig(file)
        plt.close()


        