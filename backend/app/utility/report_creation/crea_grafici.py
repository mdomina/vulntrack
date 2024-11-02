import matplotlib.pyplot as plt
import os

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

        # Crea la directory per i grafici se non esiste
        if not os.path.exists(self.graph_dir):
            os.makedirs(self.graph_dir)

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
            fig_height = max(1, len(labels) * 0.5)  # Imposta l'altezza in base al numero di etichette
        else:
            fig_height = 8
            
        # Crea una figura con altezza dinamica e larghezza fissa
        fig, ax = plt.subplots(figsize=(11, fig_height))

        # Disegna le barre orizzontali usando le etichette e le dimensioni fornite
        ax.barh(labels, sizes, color='skyblue', height=0.5)

        # Configura la dimensione dei tick delle etichette sull'asse y per migliorare la leggibilità
        if len(labels) > 15:
            ax.tick_params(axis='y', labelsize=8)

        # imposta il margine verticale tra il bordo e le barre se  i nomi delle vulnerabilità sono maggiori di 
        if len(labels) > 10:
            ax.margins(y=0.01) 
        
        # Applica un layout compatto per ridurre gli spazi bianchi
        plt.tight_layout()

        # Salva il grafico come immagine nel percorso specificato
        file = os.path.join(self.graph_dir, output_filename)
        plt.savefig(file)
        plt.close()  # Chiude la figura per liberare memoria


    # def create_timeline_chart(self, dates, critical, high, medium, low, output_filename):
    #     dates = [datetime.strptime(date, '%Y-%m-%d') for date in dates]
    #     fig, ax = plt.subplots()
    #     ax.bar(dates, critical, label='Critica', color='brown')
    #     ax.bar(dates, high, bottom=critical, label='Alta', color='red')
    #     ax.bar(dates, medium, bottom=[i + j for i, j in zip(critical, high)], label='Media', color='orange')
    #     ax.bar(dates, low, bottom=[i + j + k for i, j, k in zip(critical, high, medium)], label='Bassa', color='green')
    #     ax.set_ylabel('Numero di Vulnerabilità')
    #     ax.legend()
    #     ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    #     fig.autofmt_xdate()
    #     file = os.path.join(self.graph_dir, output_filename)
    #     plt.savefig(file)
    #     plt.close()


    def create_pie_chart(self, labels, sizes, colors, output_filename):
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
        fig, ax = plt.subplots(figsize=(6, 4))  # Riduce ulteriormente le dimensioni della figura
        bar_height = 0.3  # Imposta uno spessore delle barre più piccolo
    
        # Creazione delle barre
        ax.barh(categories, critical, label='Critica', color='brown', height=bar_height)
        ax.barh(categories, high, left=critical, label='Alta', color='red', height=bar_height)
        ax.barh(categories, medium, left=[i + j for i, j in zip(critical, high)], label='Media', color='orange', height=bar_height)
        ax.barh(categories, low, left=[i + j + k for i, j, k in zip(critical, high, medium)], label='Bassa', color='green', height=bar_height)
        # Aggiungi etichette e legenda
        # ax.set_xlabel('Numero di Vulnerabilità')
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1))  # Sposta la legenda ancora più fuori dal grafico
    
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
        axs[0].set_xlabel('Numero di Vulnerabilità')
        axs[0].set_ylabel('Tipologia')
        axs[0].invert_yaxis()

        # Recheck Histogram
        axs[1].barh(categories, data_recheck, color='lightcoral')
        axs[1].set_title('Recheck', fontsize=16, fontweight='bold')
        axs[1].set_xlabel('Numero di Vulnerabilità')
        axs[1].set_ylabel('Tipologia')
        axs[1].invert_yaxis()

        file = os.path.join(self.graph_dir, output_filename)
        plt.savefig(file, bbox_inches='tight')
        plt.close()

    def create_histogram_vuln_by_name(self, labels_vapt, sizes_vapt, labels_recheck, sizes_recheck, output_file):
        fig, axs = plt.subplots(2, 1, figsize=(16, 18), sharex=True)
        fontsize = 10

        # VAPT Vulnerability Histogram
        axs[0].barh(labels_vapt, sizes_vapt, color='skyblue')
        axs[0].set_title('VAPT', fontsize=fontsize + 2)
        axs[0].set_xlabel('Numero di Vulnerabilità', fontsize=fontsize)
        axs[0].set_ylabel('Nome della Vulnerabilità', fontsize=fontsize)
        axs[0].tick_params(axis='y', labelsize=fontsize)

        # Recheck Vulnerability Histogram
        axs[1].barh(labels_recheck, sizes_recheck, color='lightgreen')
        axs[1].set_title('Recheck', fontsize=fontsize + 2)
        axs[1].set_xlabel('Numero di Vulnerabilità', fontsize=fontsize)
        axs[1].set_ylabel('Nome della Vulnerabilità', fontsize=fontsize)
        axs[1].tick_params(axis='y', labelsize=fontsize)

        plt.subplots_adjust(left=0.3)
        file = os.path.join(self.graph_dir, output_file)
        plt.tight_layout()
        plt.savefig(file)
        plt.close()


        