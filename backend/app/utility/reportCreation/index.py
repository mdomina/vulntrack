from datetime import datetime
from docx import Document
from docx.shared import Inches
from DrawGraphs import DrawGraphs
from DrawGraphs import Recheck 
import os
from pymongo import MongoClient
from collections import Counter
from collections import defaultdict

class GeneralReport:
    def __init__(self):
        self.output_dir = 'output'
        self.graph_dir = 'grafici'
        self.template_dir = 'template'
        self.controllo_cartelle()
        self.vapt_graphs = DrawGraphs()  
        self.recheck = Recheck()       
        self.mongo_data = self.get_data_from_mongo()

    def controllo_cartelle(self):
        """Crea le cartelle necessarie se non esistono."""
        if not os.path.exists(self.graph_dir):
            os.makedirs(self.graph_dir)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        if not os.path.exists(self.template_dir):
            os.makedirs(self.template_dir)

    def get_data_from_mongo(self):
        """Ottieni i dati dalla collezione MongoDB."""
        client = MongoClient('mongodb://10.0.0.21:27017/')
        db = client['vulntrack']
        collection = db['vapt']
        return list(collection.find())
    
    def set_template(self, template_name, output_name):
        """Imposta i percorsi del template e del file di output."""
        self.template_path = os.path.join(self.template_dir, template_name)
        self.output_path = os.path.join(self.output_dir, output_name)

    def run_vapt(self):
        """Logica per generare il report VAPT."""
        # Estrazione e calcolo dei dati
        name_vapt, sizes_vapt, vuln_type_names, vuln_type_sizes, severity_names, severity_sizes = get_vuln_data_from_mongo(self.mongo_data)
        months, critical, high, medium, low = get_vuln_data_by_month(self.mongo_data)
        vapt_data, _ = get_vuln_data_for_vapt_and_recheck(self.mongo_data)
        severity_colors = ['brown', 'red', 'orange', 'green']  # I colori per ciascuna severità

        # Definizione della mappa colori per i grafici a ciambella
        severity_color_map = {
            'Critical': 'brown',
            'High': 'red',
            'Medium': 'orange',
            'Low': 'green'
        }
        donut_data = [(count, severity, severity_color_map.get(severity, 'grey'), f'{severity.lower()}.png') 
                      for severity, count in zip(severity_names, severity_sizes)]
    
        severity_labels = ['Critica', 'Alta', 'Media', 'Bassa']  # Le etichette rimangono invariate
        severity_counts_vapt = [vapt_data['Critica'], vapt_data['Alta'], vapt_data['Media'], vapt_data['Bassa']]

        # Creazione dei grafici
        self.vapt_graphs.create_horizontal_bar_chart_name(name_vapt, sizes_vapt, 'horizontal_bar_chart_by_name.png')
        self.vapt_graphs.create_timeline_chart(['2023-09-28', '2023-10-16', '2023-11-03', '2023-11-21', '2023-12-09'], [8, 1, 1, 1, 1], [4, 5, 6, 2, 1], [12, 10, 7, 9, 8], [8, 4, 2, 8, 2], 'timeline_chart.png')
        self.vapt_graphs.create_pie_chart(severity_labels, severity_counts_vapt ,severity_colors, 'pie_chart.png')
        self.vapt_graphs.create_horizontal_bar_chart_months(months, critical, high, medium, low, 'horizontal_bar_chart.png')
        self.vapt_graphs.create_bar_chart_by_category(vuln_type_names, vuln_type_sizes, 'bar_chart_by_category.png')
        self.vapt_graphs.create_all_donut_charts(donut_data, 'donut_charts.png')

        # Modifica del documento Word
        self.modify_word_document_with_charts(self.template_path, self.output_path)

    def run_recheck(self):
        """Logica per generare il report Recheck."""
        # Estrazione e calcolo dei dati
        vapt_data, recheck_data = get_vuln_data_for_vapt_and_recheck(self.mongo_data)
        vapt_counts, recheck_counts, categories = get_vuln_data_for_vapt_and_recheck_by_category(self.mongo_data)
        vapt_name_counts, recheck_name_counts, all_names = get_vuln_data_for_vapt_and_recheck_by_name(self.mongo_data)
        
        # Creazione dei grafici specifici per Recheck
        self.recheck.create_recheck_summary(list(vapt_data.values()), list(recheck_data.values()), 'recheck_summary.png')
        self.recheck.create_vapt_recheck_summary(list(vapt_data.values()), list(recheck_data.values()), 'vapt_recheck_summary.png')
        self.recheck.create_vapt_recheck_histogram(vapt_counts, recheck_counts, categories, 'vapt_recheck_histogram.png')
        self.recheck.create_histogram_vuln_by_name(all_names, vapt_name_counts, all_names, recheck_name_counts, 'vuln_histogram_by_name.png')

        # Modifica del documento Word
        self.modify_word_document_with_charts(self.template_path, self.output_path)

    def modify_word_document_with_charts(self, input_doc_path, output_doc_path):
        """Modifica un documento Word inserendo i grafici generati."""
        doc = Document(input_doc_path)
        self.replace_tag_with_chart(doc, '{{tag_graficotimeline}}', os.path.join(self.graph_dir, 'timeline_chart.png'))
        self.replace_tag_with_chart(doc, '{{tag_complessive}}', os.path.join(self.graph_dir, 'pie_chart.png'))
        self.replace_tag_with_chart(doc, '{{tag_mensili}}', os.path.join(self.graph_dir, 'horizontal_bar_chart.png'))
        self.replace_tag_with_chart(doc, '{{tag_name}}', os.path.join(self.graph_dir, 'horizontal_bar_chart_by_name.png'))
        self.replace_tag_with_chart(doc, '{{tag_categoria}}', os.path.join(self.graph_dir, 'bar_chart_by_category.png'))
        
        # Grafici per il riepilogo Recheck
        self.replace_tag_with_chart(doc, '{{tag_recheck_summary}}', os.path.join(self.graph_dir, 'recheck_summary.png'))
        self.replace_tag_with_chart(doc, '{{tag_vapt_recheck}}', os.path.join(self.graph_dir, 'vapt_recheck_summary.png'))
        self.replace_tag_with_chart(doc, '{{tag_vapt_recheck_histogram}}', os.path.join(self.graph_dir, 'vapt_recheck_histogram.png'))
        self.replace_tag_with_chart(doc, '{{tag_vuln_by_name}}', os.path.join(self.graph_dir, 'vuln_histogram_by_name.png'))
        
        # Inserimento dei grafici a ciambella (donut charts)
        self.replace_tag_with_donut_charts(doc, '{{tag_grafici_donut}}')

        # Salva il documento modificato
        doc.save(output_doc_path)

    def replace_tag_with_chart(self, doc, tag, image_path, image_width=Inches(5)):
        """Sostituisce un tag nel documento con un'immagine del grafico."""
        for paragraph in doc.paragraphs:
            if tag in paragraph.text:
                paragraph.text = ''
                paragraph.add_run().add_picture(image_path, width=image_width)

    def replace_tag_with_donut_charts(self, doc, tag):
        """Sostituisce un tag con una tabella contenente i grafici a ciambella."""
        for paragraph in doc.paragraphs:
            if tag in paragraph.text:
                paragraph.text = paragraph.text.replace(tag, '')

                table = doc.add_table(rows=1, cols=4)
                row_cells = table.rows[0].cells
                row_cells[0].paragraphs[0].add_run().add_picture(os.path.join(self.graph_dir, 'critical.png'), width=Inches(1.5))
                row_cells[1].paragraphs[0].add_run().add_picture(os.path.join(self.graph_dir, 'high.png'), width=Inches(1.5))
                row_cells[2].paragraphs[0].add_run().add_picture(os.path.join(self.graph_dir, 'medium.png'), width=Inches(1.5))
                row_cells[3].paragraphs[0].add_run().add_picture(os.path.join(self.graph_dir, 'low.png'), width=Inches(1.5))

                paragraph._element.addnext(table._element)

def get_vuln_data_by_month(mongo_data):
    severity_counts_by_month = defaultdict(lambda: {'Critica': 0, 'Alta': 0, 'Media': 0, 'Bassa': 0})
    severity_map = {'Critical': 'Critica', 'High': 'Alta', 'Medium': 'Media', 'Low': 'Bassa'}

    for item in mongo_data:
        findings = item.get('findings', [])
        date_str = item.get('date', '')  
        if date_str:
            month_number = int(date_str.split('-')[1])  
            month_name = datetime.strptime(str(month_number), "%m").strftime("%B")  
            for finding in findings:
                severity = finding.get('severity', 'Unknown')
                severity_name = severity_map.get(severity, 'Unknown')
                if severity_name in severity_counts_by_month[month_name]:
                    severity_counts_by_month[month_name][severity_name] += 1

    ordered_months = sorted(severity_counts_by_month.keys(), key=lambda x: datetime.strptime(x, "%B").month)
    months = ordered_months  
    critical_counts = [severity_counts_by_month[month]['Critica'] for month in ordered_months]
    high_counts = [severity_counts_by_month[month]['Alta'] for month in ordered_months]
    medium_counts = [severity_counts_by_month[month]['Media'] for month in ordered_months]
    low_counts = [severity_counts_by_month[month]['Bassa'] for month in ordered_months]

    return months, critical_counts, high_counts, medium_counts, low_counts

def get_vuln_data_from_mongo(mongo_data):
    findings_titles = []
    vuln_types = []  
    severities = []  
    
    for item in mongo_data:
        findings_titles.extend([finding['title'] for finding in item['findings']])
        vuln_types.extend([finding['vulnType'] for finding in item['findings']])
        severities.extend([finding['severity'] for finding in item['findings']])

    title_counts = Counter(findings_titles)
    vuln_type_counts = Counter(vuln_types)
    severity_counts = Counter(severities)
    name_vapt = list(title_counts.keys())  
    sizes_vapt = list(title_counts.values())  
    vuln_type_names = list(vuln_type_counts.keys())  
    vuln_type_sizes = list(vuln_type_counts.values())  
    severity_names = list(severity_counts.keys())  
    severity_sizes = list(severity_counts.values())  

    return name_vapt, sizes_vapt, vuln_type_names, vuln_type_sizes, severity_names, severity_sizes

def get_vuln_data_for_vapt_and_recheck(mongo_data):
    vapt_data = {'Critica': 0, 'Alta': 0, 'Media': 0, 'Bassa': 0}
    recheck_data = {'Critica': 0, 'Alta': 0, 'Media': 0, 'Bassa': 0}

    severity_map = {'Critical': 'Critica', 'High': 'Alta', 'Medium': 'Media', 'Low': 'Bassa'}

    for item in mongo_data:
        findings = item.get('findings', [])
        audit_type = item.get('auditType', 'VAPT')

        for finding in findings:
            severity = finding.get('severity', 'Unknown')
            severity_name = severity_map.get(severity, 'Unknown')

            if severity_name in vapt_data:
                if audit_type.lower() == 'recheck':
                    recheck_data[severity_name] += 1
                else:
                    vapt_data[severity_name] += 1

    return vapt_data, recheck_data

def get_vuln_data_for_vapt_and_recheck_by_category(mongo_data):
    """Dati per tipologia per VAPT e Recheck"""
    vapt_data_by_category = defaultdict(int)
    recheck_data_by_category = defaultdict(int)

    for item in mongo_data:
        findings = item.get('findings', [])
        audit_type = item.get('auditType', 'VAPT')

        for finding in findings:
            vuln_type = finding.get('vulnType', 'Unknown')
            if audit_type.lower() == 'recheck':
                recheck_data_by_category[vuln_type] += 1
            else:
                vapt_data_by_category[vuln_type] += 1

    all_categories = sorted(set(vapt_data_by_category.keys()).union(set(recheck_data_by_category.keys())))
    vapt_counts = [vapt_data_by_category[category] for category in all_categories]
    recheck_counts = [recheck_data_by_category[category] for category in all_categories]

    return vapt_counts, recheck_counts, all_categories

def get_vuln_data_for_vapt_and_recheck_by_name(mongo_data):
    """Dati per vulnerabilità per nome per VAPT e Recheck"""
    vapt_data_by_name = defaultdict(int)
    recheck_data_by_name = defaultdict(int)

    for item in mongo_data:
        findings = item.get('findings', [])
        audit_type = item.get('auditType', 'VAPT')

        for finding in findings:
            vuln_name = finding.get('title', 'Unknown')
            if audit_type.lower() == 'recheck':
                recheck_data_by_name[vuln_name] += 1
            else:
                vapt_data_by_name[vuln_name] += 1

    all_names = sorted(set(vapt_data_by_name.keys()).union(set(recheck_data_by_name.keys())))
    vapt_counts = [vapt_data_by_name[name] for name in all_names]
    recheck_counts = [recheck_data_by_name[name] for name in all_names]

    return vapt_counts, recheck_counts, all_names

# Funzione per sostituire i tag nel documento Word con immagini
def replace_tag_with_chart(doc, tag, image_path, image_width=Inches(5)):
    for paragraph in doc.paragraphs:
        if tag in paragraph.text:
            paragraph.text = ''
            paragraph.add_run().add_picture(image_path, width=image_width)

if __name__ == '__main__':
    # Esempio di utilizzo della classe GeneralReport per generare report VAPT e Recheck
    report_generator_dashboard = GeneralReport()
    report_generator_dashboard.set_template('dashboard.docx', 'output_report_dashboard.docx')
    report_generator_dashboard.run_vapt()

    report_generator_recheck = GeneralReport()
    report_generator_recheck.set_template('recheck.docx', 'output_report_recheck.docx')
    report_generator_recheck.run_recheck()
