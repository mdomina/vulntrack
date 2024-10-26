import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from datetime import datetime
graph_dir = 'grafici'

if not os.path.exists(graph_dir):
    os.makedirs(graph_dir)

    
class DrawGraphs:
    def __init__(self):
        pass

    # Funzione per creare un grafico a barre orizzontali
    def create_horizontal_bar_chart_name(self, labels, sizes, output_filename):
        fig, ax = plt.subplots(figsize=(10, 8))  # Aumenta la dimensione della figura

        # Creazione del grafico a barre orizzontali
        ax.barh(labels, sizes, color='skyblue', height=0.5)  # Riduci l'altezza delle barre
        ax.set_xlabel('Numero di Vulnerabilità')
        ax.set_ylabel('Nome Vulnerabilità')
        ax.tick_params(axis='y', labelsize=8)  # Imposta la dimensione del font per l'asse Y
        plt.tight_layout()
        # Salva il file
        file = os.path.join(graph_dir, output_filename)
        plt.savefig(file)
        plt.close()

    # Funzione per creare il grafico della timeline delle vulnerabilità
    def create_timeline_chart(self, dates, critical, high, medium, low, output_filename):
        dates = [datetime.strptime(date, '%Y-%m-%d') for date in dates]
        fig, ax = plt.subplots()
        ax.bar(dates, critical, label='Critica', color='brown')
        ax.bar(dates, high, bottom=critical, label='Alta', color='red')
        ax.bar(dates, medium, bottom=[i+j for i,j in zip(critical, high)], label='Media', color='orange')
        ax.bar(dates, low, bottom=[i+j+k for i,j,k in zip(critical, high, medium)], label='Bassa', color='green')
        ax.set_ylabel('Numero di Vulnerabilità')
        ax.legend()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
        fig.autofmt_xdate()
        file = os.path.join(graph_dir, output_filename)
        plt.savefig(file)
        plt.close()

    # Funzione per creare il grafico a torta della percentuale di vulnerabilità complessive
    def create_pie_chart(self, labels, sizes, colors, output_filename):
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.axis('equal')
        file = os.path.join(graph_dir, output_filename)
        plt.savefig(file)
        plt.close()

    # Funzione per creare un istogramma (grafico a barre verticali) per Vulnerabilità per Categoria
    def create_bar_chart_by_category(self, labels, sizes, output_filename):
        fig, ax = plt.subplots()
        ax.bar(labels, sizes, color='skyblue')
        ax.set_ylabel('Numero di Vulnerabilità')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        file = os.path.join(graph_dir, output_filename)
        plt.savefig(file)
        plt.close()

    # Funzione per creare un grafico a barre orizzontali impilate
    def create_horizontal_bar_chart_months(self, categories, critical, high, medium, low, output_filename):
        fig, ax = plt.subplots()
        ax.barh(categories, critical, label='Critica', color='brown')
        ax.barh(categories, high, left=critical, label='Alta', color='red')
        ax.barh(categories, medium, left=[i+j for i,j in zip(critical, high)], label='Media', color='orange')
        ax.barh(categories, low, left=[i+j+k for i,j,k in zip(critical, high, medium)], label='Bassa', color='green')
        ax.set_xlabel('Numero di Vulnerabilità')
        ax.legend()
        file = os.path.join(graph_dir, output_filename)
        plt.savefig(file)
        plt.close()

    def create_donut_chart(self, value, label, color, output_filename):
        fig, ax = plt.subplots()

        # Calcola il resto per completare la ciambella (se il totale è il valore passato)
        total = value if value > 0 else 1  # Imposta un minimo di 1 per evitare valori negativi o zero
        remainder = total - value

        # Usa il valore effettivo per il wedge (ciambella) e il resto per riempire lo spazio
        ax.pie([value, remainder], labels=[label, ''], startangle=90, colors=[color, 'lightgrey'], 
            wedgeprops={'width': 0.3, 'edgecolor': 'white'}, 
            textprops={'fontsize': 20, 'color': 'black'})

        # Aggiungi il numero al centro della ciambella
        ax.text(0, 0, str(value), ha='center', va='center', fontsize=24, color=color)
        ax.axis('equal')

        # Salva il grafico
        plt.savefig(os.path.join(graph_dir, output_filename), transparent=True)
        plt.close()


    # Funzione per creare tutti i grafici a ciambella
    def create_all_donut_charts(self, data, output_filenames):
        for value, label, color, filename in data:
            self.create_donut_chart(value, label, color, filename)


    # Funzione per creare un grafico a barre
    def create_bar_chart(self, categories, critical, high, medium, low, output_filename):
        fig, ax = plt.subplots()
        ax.bar(categories, critical, label='Critica', color='red', bottom=[high[j] + medium[j] + low[j] for j in range(len(categories))])
        ax.bar(categories, high, label='Alta', color='orange', bottom=[medium[j] + low[j] for j in range(len(categories))])
        ax.bar(categories, medium, label='Media', color='yellow', bottom=low)
        ax.bar(categories, low, label='Bassa', color='green')
        ax.set_ylabel('Numero di Vulnerabilità')
        ax.legend()
        file = os.path.join(graph_dir, output_filename)
        plt.savefig(file)
        plt.close()



class Recheck:
    def __init__(self):
        pass

class Recheck:
    def create_recheck_summary(self, data_vapt, data_recheck, output_filename):
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))

        # Colori e nomi
        categories = ['Critiche', 'Alte', 'Medie', 'Basse']
        colors = ['brown', 'red', 'orange', 'green']
        # Spaziatura verticale per evitare sovrapposizioni
        y_positions = [0.8, 0.55, 0.3, 0.05]
        # VAPT
        for i, (value, category, color) in enumerate(zip(data_vapt, categories, colors)):
            axs[0].text(0.5, y_positions[i], f'{value}\n{category}', color='white',
                        ha='center', va='center', fontsize=16, fontweight='bold',
                        bbox=dict(facecolor=color, edgecolor=color, boxstyle='round,pad=0.6'))

        axs[0].axis('off')
        axs[0].set_title('VAPT', fontsize=16, fontweight='bold', y=1.05)  # Posiziona il titolo sopra i quadrati
        # Recheck
        for i, (value, category, color) in enumerate(zip(data_recheck, categories, colors)):
            axs[1].text(0.5, y_positions[i], f'{value}\n{category}', color='white',
                        ha='center', va='center', fontsize=16, fontweight='bold',
                        bbox=dict(facecolor=color, edgecolor=color, boxstyle='round,pad=0.6'))

        axs[1].axis('off')
        axs[1].set_title('Recheck', fontsize=16, fontweight='bold', y=1.05)  # Posiziona il titolo sopra i quadrati

        file = os.path.join(graph_dir, output_filename)
        plt.savefig(file, bbox_inches='tight')
        plt.close()


    def create_vapt_recheck_summary(self, data_vapt, data_recheck, output_filename):
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))
        # Etichette e colori
        categories = ['Critica', 'Alta', 'Media', 'Bassa']
        colors = ['brown', 'red', 'orange', 'green']
        # Grafico VAPT
        for i, (value, category, color) in enumerate(zip(data_vapt, categories, colors)):
            axs[0].barh(category, value, color=color)
            axs[0].text(value, i, f'{value}', color='white', va='center', fontsize=12, fontweight='bold')
        axs[0].set_xlim(0, max(data_vapt) + 1)
        axs[0].set_title('VAPT', fontsize=16, fontweight='bold')
        # Grafico Recheck
        for i, (value, category, color) in enumerate(zip(data_recheck, categories, colors)):
            axs[1].barh(category, value, color=color)
            axs[1].text(value, i, f'{value}', color='white', va='center', fontsize=12, fontweight='bold')
        axs[1].set_xlim(0, max(data_recheck) + 1)
        axs[1].set_title('Recheck', fontsize=16, fontweight='bold')

        # Aggiunta della legenda
        plt.figlegend(categories, loc='lower center', ncol=4, labelspacing=1, prop={'size': 12})

        # Impostazione del titolo generale
      #  plt.suptitle('Vulnerabilità Totali', fontsize=20, fontweight='bold', y=0.98)
        
        # Salvataggio del file
        file = os.path.join(graph_dir, output_filename)
        plt.savefig(file, bbox_inches='tight')
        plt.close()

    def create_vapt_recheck_histogram(self, data_vapt, data_recheck, categories, output_filename):
        fig, axs = plt.subplots(2, 1, figsize=(10, 10))  # Creiamo due subplots in verticale (2 righe, 1 colonna)

        # Grafico VAPT
        axs[0].barh(categories, data_vapt, color='skyblue')  # Usa barh per un grafico a barre orizzontali
        axs[0].set_title('VAPT', fontsize=16, fontweight='bold')
        axs[0].set_xlabel('Numero di Vulnerabilità')
        axs[0].set_ylabel('Tipologia')  # Assegna il nome all'asse Y
        axs[0].invert_yaxis()  # Inverti l'asse Y per avere i valori maggiori in cima

        # Grafico Recheck
        axs[1].barh(categories, data_recheck, color='lightcoral')  # Anche qui un grafico a barre orizzontali
        axs[1].set_title('Recheck', fontsize=16, fontweight='bold')
        axs[1].set_xlabel('Numero di Vulnerabilità')
        axs[1].set_ylabel('Tipologia')
        axs[1].invert_yaxis()  # Inverti l'asse Y per mantenere coerenza con l'altro grafico

        # Salvataggio del file
        file = os.path.join(graph_dir, output_filename)
        plt.savefig(file, bbox_inches='tight')
        plt.close()
    
    # Funzione per creare un istogramma per le vulnerabilità per nome
    def create_histogram_vuln_by_name(self, labels_vapt, sizes_vapt, labels_recheck, sizes_recheck, output_file):
        # Crea una figura con due subplot in due righe, uno sotto l'altro
        fig, axs = plt.subplots(2, 1, figsize=(16, 18), sharex=True)

        # Riduci la dimensione del testo per migliorare la leggibilità
        fontsize = 10

        # Creazione dell'istogramma per VAPT
        axs[0].barh(labels_vapt, sizes_vapt, color='skyblue')
        axs[0].set_title('VAPT', fontsize=fontsize + 2)
        axs[0].set_xlabel('Numero di Vulnerabilità', fontsize=fontsize)
        axs[0].set_ylabel('Nome della Vulnerabilità', fontsize=fontsize)
        axs[0].tick_params(axis='y', labelsize=fontsize)  # Riduci la dimensione del testo delle etichette

        # Creazione dell'istogramma per Recheck
        axs[1].barh(labels_recheck, sizes_recheck, color='lightgreen')
        axs[1].set_title('Recheck', fontsize=fontsize + 2)
        axs[1].set_xlabel('Numero di Vulnerabilità', fontsize=fontsize)
        axs[1].set_ylabel('Nome della Vulnerabilità', fontsize=fontsize)
        axs[1].tick_params(axis='y', labelsize=fontsize)  # Riduci la dimensione del testo delle etichette

        # Aumenta lo spazio tra le etichette e le barre per evitare sovrapposizioni
        plt.subplots_adjust(left=0.3)  # Aumenta lo spazio a sinistra per il testo

        # Salva il grafico
        file = os.path.join(graph_dir, output_file)

        # Ottimizza la disposizione degli elementi
        plt.tight_layout()
        plt.savefig(file)
        plt.close()



        