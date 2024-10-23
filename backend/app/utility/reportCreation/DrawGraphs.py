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
    def create_bar_chart_by_name(self):
        labels = ['Software Vulnerabilità', 'Bug Fixing', 'Vulnerabilità Javascript', 'SQL Injection', 'Buffer Overflow', 
                  'Cross-Site Scripting', 'Access Control Issues', 'Other']
        sizes = [20, 15, 10, 8, 7, 6, 5, 3]
        fig, ax = plt.subplots()
        ax.bar(labels, sizes, color='skyblue')
        ax.set_ylabel('Numero di Vulnerabilità')
        ax.set_title('Vulnerabilità per Nome')

        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        file = os.path.join(graph_dir, 'bar_chart_by_name.png')
        plt.savefig(file)
        plt.close()

    # Funzione per creare il grafico della timeline delle vulnerabilità
    def create_timeline_chart(self):
        dates = ['2023-09-28', '2023-10-16', '2023-11-03', '2023-11-21', '2023-12-09']
        dates = [datetime.strptime(date, '%Y-%m-%d') for date in dates]
        
        critical = [8, 1, 1, 1, 1]
        high = [4, 5, 6, 2, 1]
        medium = [12, 10, 7, 9, 8]
        low = [8, 4, 2, 8, 2]

        fig, ax = plt.subplots()
        ax.bar(dates, critical, label='Critica', color='brown')
        ax.bar(dates, high, bottom=critical, label='Alta', color='red')
        ax.bar(dates, medium, bottom=[i+j for i,j in zip(critical, high)], label='Media', color='orange')
        ax.bar(dates, low, bottom=[i+j+k for i,j,k in zip(critical, high, medium)], label='Bassa', color='green')

        ax.set_ylabel('Numero di Vulnerabilità')
        ax.set_title('Timeline Vulnerabilità')
        ax.legend()

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
        fig.autofmt_xdate()
        file = os.path.join(graph_dir, 'timeline_chart.png')
        plt.savefig(file)
        plt.close()

    # Funzione per creare il grafico a torta della percentuale di vulnerabilità complessive
    def create_pie_chart(self):
        labels = ['Critica', 'Alta', 'Media', 'Bassa']
        sizes = [8, 21, 164, 88]
        colors = ['brown', 'red', 'orange', 'green']
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.axis('equal')
        plt.title('Percentuale Vulnerabilità Complessive')
        file = os.path.join(graph_dir, 'pie_chart.png')
        plt.savefig(file)
        plt.close()
    # Funzione per creare un istogramma (grafico a barre verticali) per Vulnerabilità per Categoria
    def create_bar_chart_by_category(self):
        labels = ['Broken Access Control', 'Identification And Auth', 'Cryptographic Failures', 
                  'Insecure Design', 'Vulnerable And Outdated Components',
                  'Authentication Failures', 'Resource Design']
        sizes = [40, 24, 36, 34, 38, 32, 1]  # Valori fittizi simili allo screenshot

        fig, ax = plt.subplots()
        ax.bar(labels, sizes, color='skyblue')
        ax.set_ylabel('Numero di Vulnerabilità')
        ax.set_title('Vulnerabilità per Categoria')

        plt.xticks(rotation=45, ha='right')  # Ruota le etichette per migliorare la leggibilità
        plt.tight_layout()  # Ottimizza lo spazio

        file = os.path.join(graph_dir, 'bar_chart_by_category.png')  # Salva il grafico
        plt.savefig(file)
        plt.close()


    # Funzione per creare un grafico a barre orizzontali impilate
    def create_horizontal_bar_chart(self):
        categories = ['Settembre', 'Ottobre', 'Novembre', 'Dicembre']
        critical = [8, 3, 3, 5]
        high = [12, 6, 6, 12]
        medium = [12, 35, 47, 74]
        low = [12, 67, 79, 123]

        fig, ax = plt.subplots()
        ax.barh(categories, critical, label='Critica', color='brown')
        ax.barh(categories, high, left=critical, label='Alta', color='red')
        ax.barh(categories, medium, left=[i+j for i,j in zip(critical, high)], label='Media', color='orange')
        ax.barh(categories, low, left=[i+j+k for i,j,k in zip(critical, high, medium)], label='Bassa', color='green')

        ax.set_xlabel('Numero di Vulnerabilità')
        ax.set_title('Vulnerabilità Complessive Mensili')
        ax.legend()
        file = os.path.join(graph_dir, 'horizontal_bar_chart.png')
        plt.savefig(file)
        plt.close()

    # Funzione per creare un singolo grafico a ciambella per una categoria
    def create_donut_chart(self, value, label, color, filename):
        fig, ax = plt.subplots()
        ax.pie([value, 1], labels=[label, ''], startangle=90, colors=[color, 'lightgrey'], 
               wedgeprops={'width': 0.3, 'edgecolor': 'white'}, 
               textprops={'fontsize': 14, 'color': 'black'}, autopct=lambda p: f'{value}' if p > 0 else '')
        ax.text(0, 0, str(value), ha='center', va='center', fontsize=24, color=color)
        ax.axis('equal')
        plt.savefig(os.path.join(graph_dir, filename), transparent=True)
        plt.close()

    # Creazione di 4 grafici a ciambella
    def create_all_donut_charts(self):
        self.create_donut_chart(8, 'Critiche', 'brown', 'critiche.png')
        self.create_donut_chart(21, 'Alte', 'red', 'alte.png')
        self.create_donut_chart(164, 'Medie', 'orange', 'medie.png')
        self.create_donut_chart(88, 'Basse', 'green', 'basse.png')

    # Funzione per creare un grafico a barre
    def create_bar_chart(self):
        categories = ['Settembre', 'Ottobre', 'Novembre', 'Dicembre']
        critical = [8, 35, 47, 12]
        high = [12, 23, 29, 74]
        medium = [67, 67, 79, 122]
        low = [12, 67, 79, 123]

        fig, ax = plt.subplots()
        ax.bar(categories, critical, label='Critica', color='red', bottom=[high[j] + medium[j] + low[j] for j in range(len(categories))])
        ax.bar(categories, high, label='Alta', color='orange', bottom=[medium[j] + low[j] for j in range(len(categories))])
        ax.bar(categories, medium, label='Media', color='yellow', bottom=low)
        ax.bar(categories, low, label='Bassa', color='green')

        ax.set_ylabel('Numero di Vulnerabilità')
        ax.set_title('Vulnerabilità per Mese')
        ax.legend()
        file = os.path.join(graph_dir, 'bar_chart.png')
        plt.savefig(file)
        plt.close()
