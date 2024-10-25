from datetime import datetime
from docx import Document
from docx.shared import Inches
from DrawGraphs import DrawGraphs
from DrawGraphs import Recheck  # Importa la classe Recheck
import os
from pymongo import MongoClient
from collections import Counter
from collections import defaultdict

# Inizializza la classe DrawGraphs
draw_graphs = DrawGraphs()

# Inizializza la classe Recheck
recheck = Recheck()

# Connessione al database MongoDB
client = MongoClient('mongodb://10.0.0.21:27017/')  # Sostituisci con l'URI corretto se necessario
db = client['vulntrack']  # Nome del database
collection = db['vapt']  # Nome della collezione

output_dir = 'output'
graph_dir = 'grafici'

if not os.path.exists(graph_dir):
    os.makedirs(graph_dir)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

template_dir = 'template'

if not os.path.exists(template_dir):
    os.makedirs(template_dir)


def get_data_from_mongo():
    data = list(collection.find())  # Trova tutti i documenti nella collezione
    return data

mongo_data = get_data_from_mongo()

def get_vuln_data_by_month():

    # Dobbiamo contare le vulnerabilità per severità e mese
    severity_counts_by_month = defaultdict(lambda: {'Critica': 0, 'Alta': 0, 'Media': 0, 'Bassa': 0})

    # Mappa per associare la severità ai nomi che useremo nel grafico
    severity_map = {
        'Critical': 'Critica',
        'High': 'Alta',
        'Medium': 'Media',
        'Low': 'Bassa'
    }

    for item in mongo_data:
        # Estrai la data della vulnerabilità e converti il mese in formato leggibile (es. "Settembre")
        findings = item.get('findings', [])
        date_str = item.get('date', '')  # Assumiamo che la data sia nel formato YYYY-MM-DD
        if date_str:
            month_number = int(date_str.split('-')[1])  # Estrai il mese dalla data (es. '09' da '2023-09-27')
            month_name = datetime.strptime(str(month_number), "%m").strftime("%B")  # Converte il mese in nome

            # Conta le severità delle vulnerabilità nel mese corrente
            for finding in findings:
                severity = finding.get('severity', 'Unknown')
                severity_name = severity_map.get(severity, 'Unknown')

                if severity_name in severity_counts_by_month[month_name]:
                    severity_counts_by_month[month_name][severity_name] += 1

    # Ordiniamo i mesi in base all'ordine cronologico
    ordered_months = sorted(severity_counts_by_month.keys(), key=lambda x: datetime.strptime(x, "%B").month)
    
    # Ritorniamo i mesi e i conteggi per ciascuna severità
    months = ordered_months
    critical_counts = [severity_counts_by_month[month]['Critica'] for month in months]
    high_counts = [severity_counts_by_month[month]['Alta'] for month in months]
    medium_counts = [severity_counts_by_month[month]['Media'] for month in months]
    low_counts = [severity_counts_by_month[month]['Bassa'] for month in months]

    return months, critical_counts, high_counts, medium_counts, low_counts

def get_vuln_data_from_mongo():
    # Estrai tutti i documenti da MongoDB

    # Estrai i titoli delle vulnerabilità e i tipi di vulnerabilità da tutti i documenti
    findings_titles = []
    vuln_types = []  # Nuovo elenco per memorizzare i vulnType
    severities = []  # Nuovo elenco per memorizzare le severity
    
    for item in mongo_data:
        # Ottieni il titolo, il tipo e la gravità (severity) di ciascuna vulnerabilità all'interno di findings
        findings_titles.extend([finding['title'] for finding in item['findings']])
        vuln_types.extend([finding['vulnType'] for finding in item['findings']])  # Estrai i vulnType
        severities.extend([finding['severity'] for finding in item['findings']])  # Estrai la severity

    # Usa Counter per contare le occorrenze di ciascun titolo, vulnType e severity
    title_counts = Counter(findings_titles)
    vuln_type_counts = Counter(vuln_types)
    severity_counts = Counter(severities)

    # Ritorna i titoli unici, la loro frequenza, i vulnType unici, il loro conteggio e le severity
    name_vapt = list(title_counts.keys())  # Titoli unici delle vulnerabilità
    sizes_vapt = list(title_counts.values())  # Frequenza di ciascuna vulnerabilità
    vuln_type_names = list(vuln_type_counts.keys())  # VulnType unici
    vuln_type_sizes = list(vuln_type_counts.values())  # Frequenza di ciascun vulnType
    severity_names = list(severity_counts.keys())  # Severities uniche
    severity_sizes = list(severity_counts.values())  # Frequenza di ciascuna severity

    return name_vapt, sizes_vapt, vuln_type_names, vuln_type_sizes, severity_names, severity_sizes

name_vapt, sizes_vapt, vuln_type_names, vuln_type_sizes, severity_names, severity_sizes = get_vuln_data_from_mongo()

months, critical, high, medium, low = get_vuln_data_by_month()

# Funzione per sostituire i tag nel documento Word
def replace_tag_with_chart(doc, tag, image_path, image_width=Inches(5)):
    for paragraph in doc.paragraphs:
        if tag in paragraph.text:
            paragraph.text = ''
            paragraph.add_run().add_picture(image_path, width=image_width)

def replace_tag_with_donut_charts(doc, tag):
    for paragraph in doc.paragraphs:
        if tag in paragraph.text:
            paragraph.text = paragraph.text.replace(tag, '')

            table = doc.add_table(rows=1, cols=4)

            row_cells = table.rows[0].cells
            row_cells[0].paragraphs[0].add_run().add_picture(os.path.join(graph_dir, 'critiche.png'), width=Inches(1.5))
            row_cells[1].paragraphs[0].add_run().add_picture(os.path.join(graph_dir, 'alte.png'), width=Inches(1.5))
            row_cells[2].paragraphs[0].add_run().add_picture(os.path.join(graph_dir, 'medie.png'), width=Inches(1.5))
            row_cells[3].paragraphs[0].add_run().add_picture(os.path.join(graph_dir, 'basse.png'), width=Inches(1.5))
            
            paragraph._element.addnext(table._element)

# Funzione per leggere e modificare un documento Word esistente
def modify_word_document_with_charts(input_doc_path, output_doc_path, mongo_data):
    doc = Document(input_doc_path)

    # Dati per i grafici
    # Estrai i dati dalla risposta MongoDB per usarli nei grafici
    labels_recheck = ['Buffer Overflow', 'Cross-Site Scripting', 'SQL Injection', 'Weak Password Requirements']
    sizes_recheck = [10, 8, 6, 4]
    
    data_vapt = [0, 0, 11, 6]  # Dati per VAPT
    data_recheck = [0, 0, 2, 3]  # Dati per Recheck
    
 # Crea i dati per i grafici a ciambella sulla base della severity
    severity_color_map = {
        'Critica': 'brown',
        'Alta': 'red',
        'Media': 'orange',
        'Bassa': 'green'
    }
    
    donut_data = [(count, severity, severity_color_map.get(severity, 'grey'), f'{severity.lower()}.png') for severity, count in zip(severity_names, severity_sizes)]
   
    data_vapt_tipologia = [4, 1, 2, 4, 6]
    data_recheck_tipologia = [2, 0, 1, 2, 4]
    categories = ['Security Misconfiguration', 'Identification', 'Cryptographic Failures', 'Injection', 'Insecure Design']


    # Genera i grafici usando la classe DrawGraphs
    draw_graphs.create_horizontal_bar_chart_name(name_vapt, sizes_vapt, 'horizontal_bar_chart_by_name.png')
    draw_graphs.create_timeline_chart(['2023-09-28', '2023-10-16', '2023-11-03', '2023-11-21', '2023-12-09'], [8, 1, 1, 1, 1], [4, 5, 6, 2, 1], [12, 10, 7, 9, 8], [8, 4, 2, 8, 2], 'timeline_chart.png')
    draw_graphs.create_pie_chart(['Critica', 'Alta', 'Media', 'Bassa'], [8, 21, 164, 88], ['brown', 'red', 'orange', 'green'], 'pie_chart.png')
    draw_graphs.create_horizontal_bar_chart_months(months, critical, high, medium, low, 'horizontal_bar_chart.png')
    draw_graphs.create_all_donut_charts(donut_data, 'donut_charts.png')
    draw_graphs.create_bar_chart_by_category(vuln_type_names,vuln_type_sizes, 'bar_chart_by_category.png')

    # Genera il grafico di riepilogo Recheck usando la classe Recheck
    recheck.create_recheck_summary(data_vapt, data_recheck, 'recheck_summary.png')
    recheck.create_vapt_recheck_summary(data_vapt, data_recheck, 'vapt_recheck_summary.png')
    recheck.create_vapt_recheck_histogram(data_vapt_tipologia, data_recheck_tipologia, categories, 'vapt_recheck_histogram.png')
    recheck.create_histogram_vuln_by_name(name_vapt, sizes_vapt, labels_recheck, sizes_recheck, 'vuln_histogram_by_name.png')

    # Sostituisci i tag con i grafici
    replace_tag_with_chart(doc, '{{tag_graficotimeline}}', os.path.join(graph_dir, 'timeline_chart.png'))
    replace_tag_with_chart(doc, '{{tag_complessive}}', os.path.join(graph_dir, 'pie_chart.png'))
    replace_tag_with_chart(doc, '{{tag_mensili}}', os.path.join(graph_dir, 'horizontal_bar_chart.png'))
    replace_tag_with_chart(doc, '{{tag_name}}', os.path.join(graph_dir, 'horizontal_bar_chart_by_name.png'))
    replace_tag_with_chart(doc, '{{tag_categoria}}', os.path.join(graph_dir, 'bar_chart_by_category.png'))

    # Sostituisci il grafico di riepilogo Recheck
    replace_tag_with_chart(doc, '{{tag_recheck_summary}}', os.path.join(graph_dir, 'recheck_summary.png'))
    replace_tag_with_chart(doc, '{{tag_vapt_recheck}}', os.path.join(graph_dir, 'vapt_recheck_summary.png'))
    replace_tag_with_chart(doc, '{{tag_vapt_recheck_histogram}}', os.path.join(graph_dir, 'vapt_recheck_histogram.png'))
    replace_tag_with_chart(doc, '{{tag_vuln_by_name}}', os.path.join(graph_dir, 'vuln_histogram_by_name.png'))

    replace_tag_with_donut_charts(doc, '{{tag_grafici_donut}}')

    # Salva il documento modificato
    doc.save(output_doc_path)

# Esecuzione del codice per modificare il documento con i grafici
file_template_dashboard = os.path.join(template_dir, 'dashboard.docx')
file_output_dashboard = os.path.join(output_dir, 'output_report_dashboard.docx')

file_template_recheck = os.path.join(template_dir, 'recheck.docx')
file_output_recheck = os.path.join(output_dir, 'output_report_recheck.docx')

mongo_data = get_data_from_mongo()
modify_word_document_with_charts(file_template_dashboard, file_output_dashboard, mongo_data)
modify_word_document_with_charts(file_template_recheck, file_output_recheck, mongo_data)
