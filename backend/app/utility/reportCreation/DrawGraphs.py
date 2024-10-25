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

    # Funzione per creare il grafico a barre delle vulnerabilità per nome
    def create_bar_chart_by_name(self, labels, sizes, output_filename):
        fig, ax = plt.subplots()
        ax.bar(labels, sizes, color='skyblue')
        ax.set_ylabel('Numero di Vulnerabilità')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
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
    def create_horizontal_bar_chart(self, categories, critical, high, medium, low, output_filename):
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

    # Funzione per creare un singolo grafico a ciambella per una categoria senza spazio bianco
    def create_donut_chart(self, value, label, color, output_filename):
        fig, ax = plt.subplots()
        ax.pie([value, 0], labels=[label, ''], startangle=90, colors=[color, 'lightgrey'], 
            wedgeprops={'width': 0.3, 'edgecolor': 'white'}, 
            textprops={'fontsize': 20, 'color': 'black'})
        ax.text(0, 0, str(value), ha='center', va='center', fontsize=24, color=color)
        ax.axis('equal')
        plt.savefig(os.path.join(graph_dir, output_filename), transparent=True)
        plt.close()

    # Creazione di 4 grafici a ciambella senza spazi bianchi
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

    # Funzione per creare i quadrati colorati che rappresentano le vulnerabilità
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

      #  plt.suptitle('Recheck Summary', fontsize=20, fontweight='bold', y=1.1)  # Sposta il titolo principale un po' più in alto
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

        # Funzione per creare l'istogramma Vulnerabilità per Tipologia (sostituzione del radar chart)
    def create_vapt_recheck_histogram(self, data_vapt, data_recheck, categories, output_filename):
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))

        # Grafico VAPT
        axs[0].bar(categories, data_vapt, color='skyblue')
        axs[0].set_title('VAPT', fontsize=16, fontweight='bold')
        axs[0].set_xlabel('Tipologia')
        axs[0].set_ylabel('Numero di Vulnerabilità')
        axs[0].tick_params(axis='x', rotation=45)

        # Grafico Recheck
        axs[1].bar(categories, data_recheck, color='lightcoral')
        axs[1].set_title('Recheck', fontsize=16, fontweight='bold')
        axs[1].set_xlabel('Tipologia')
        axs[1].set_ylabel('Numero di Vulnerabilità')
        axs[1].tick_params(axis='x', rotation=45)

        # Impostazione del titolo generale
       # plt.suptitle('Vulnerabilità per Tipologia', fontsize=20, fontweight='bold', y=1.02)

        # Salvataggio del file
        file = os.path.join(graph_dir, output_filename)
        plt.savefig(file, bbox_inches='tight')
        plt.close()
    
        # Funzione per creare un istogramma per le vulnerabilità per nome
    def create_histogram_vuln_by_name(self, labels_vapt, sizes_vapt, labels_recheck, sizes_recheck, output_file):
        fig, axs = plt.subplots(1, 2, figsize=(12, 6), sharey=True)

        # Creazione dell'istogramma per VAPT
        axs[0].barh(labels_vapt, sizes_vapt, color='skyblue')
        axs[0].set_title('VAPT')
        axs[0].set_xlabel('Numero di Vulnerabilità')
        axs[0].set_ylabel('Nome della Vulnerabilità')

        # Creazione dell'istogramma per Recheck
        axs[1].barh(labels_recheck, sizes_recheck, color='lightgreen')
        axs[1].set_title('Recheck')
        axs[1].set_xlabel('Numero di Vulnerabilità')

        file = os.path.join(graph_dir, output_file)

        plt.tight_layout()
        plt.savefig(file)
        plt.close()

        