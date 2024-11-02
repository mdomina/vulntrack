from datetime import datetime
from docx import Document
from docx.shared import Inches
from app.utility.report_creation.crea_grafici import Dashboard, Recheck
import os
from collections import Counter
from collections import defaultdict
import subprocess
from app.utility.report_creation.modifica_template import ModificaTemplate
from app.utility.report_creation.format_data import get_vuln_data_by_month
from app.utility.report_creation.format_data import get_vuln_data_from_mongo
from app.utility.report_creation.format_data import get_vuln_data_for_vapt_and_recheck
from app.utility.report_creation.format_data import get_vuln_data_for_vapt_and_recheck_by_category
from app.utility.report_creation.format_data import get_vuln_data_for_vapt_and_recheck_by_name


class GeneralReport:
    def __init__(self, mongo_data):
        base_dir = os.path.dirname(__file__)  # Directory corrente dove si trova `index.py`  
        self.output_dir = os.path.join(base_dir, 'output') 
        self.graph_dir = os.path.join(base_dir, 'grafici') 
        self.template_dir = os.path.join(base_dir, 'template')
        self.controllo_cartelle()
        self.vapt_graphs = Dashboard()  
        self.recheck = Recheck()      
        self.mongo_data = mongo_data   

    def controllo_cartelle(self):
        """Crea le cartelle necessarie se non esistono."""
        if not os.path.exists(self.graph_dir):
            os.makedirs(self.graph_dir)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        if not os.path.exists(self.template_dir):
            os.makedirs(self.template_dir)
    
    def set_template(self, template_name, output_name):
        """Imposta i percorsi del template e del file di output."""
        self.template_path = os.path.join(self.template_dir, template_name)
        self.output_path = os.path.join(self.output_dir, output_name)

    def run_vapt(self):
        
        is_recheck = any(item.get('auditType', '').lower() == 'recheck' for item in self.mongo_data)

        """Logica per generare il report VAPT."""
        # Estrazione e calcolo dei dati
        name_vapt, sizes_vapt, vuln_type_names, vuln_type_sizes, severity_names, severity_sizes = get_vuln_data_from_mongo(self.mongo_data)
        months, critical, high, medium, low = get_vuln_data_by_month(self.mongo_data)
        vapt_data, recheck_data = get_vuln_data_for_vapt_and_recheck(self.mongo_data)  # Ottieni sia vapt_data che recheck_data
        severity_colors = ['brown', 'red', 'orange', 'green']  # I colori per ciascuna severità
        # Definizione della mappa colori per i grafici a ciambella
        severity_color_map = {
            'Critical': 'brown',
            'High': 'red',
            'Medium': 'orange',
            'Low': 'green'
        }
        
        if is_recheck:
            donut_data = [(count, severity, severity_color_map.get(severity, 'grey'), f'{severity.lower()}.png') 
                        for severity, count in zip(severity_names, recheck_data.values())]
            pie_chart_data = list(recheck_data.values())
            pie_chart_name = 'pie_chart_recheck.png'
            
        else:
            donut_data = [(count, severity, severity_color_map.get(severity, 'grey'), f'{severity.lower()}.png') 
                        for severity, count in zip(severity_names, vapt_data.values())]
            pie_chart_data = list(vapt_data.values())
            pie_chart_name = 'pie_chart_vapt.png'
      
        self.vapt_graphs.horizontal_bar_chart_by_name(name_vapt, sizes_vapt, os.path.join(self.graph_dir, 'horizontal_bar_chart_by_name.png'))
        # self.vapt_graphs.create_timeline_chart(
        #     ['2023-09-28', '2023-10-16', '2023-11-03', '2023-11-21', '2023-12-09'],
        #     [8, 1, 1, 1, 1], [4, 5, 6, 2, 1], [12, 10, 7, 9, 8], [8, 4, 2, 8, 2],
        #     os.path.join(self.graph_dir, 'timeline_chart.png')
        # )
        self.vapt_graphs.create_pie_chart(severity_names, pie_chart_data, severity_colors, os.path.join(self.graph_dir, pie_chart_name))
        self.vapt_graphs.create_horizontal_bar_chart_months(months, critical, high, medium, low, os.path.join(self.graph_dir, 'horizontal_bar_chart.png'))
        self.vapt_graphs.create_bar_chart_by_category(vuln_type_names, vuln_type_sizes, os.path.join(self.graph_dir, 'bar_chart_by_category.png'))

        # Creazione di grafici a ciambella per ciascuna severità sia per VAPT che per Recheck
        self.vapt_graphs.create_all_donut_charts(donut_data)

        # Modifica del documento Word
        mt = ModificaTemplate(
            self.template_path, 
            self.output_path,
            self.graph_dir,
            )
        mt.modify_word_document_with_charts(self.mongo_data)

    def run_recheck(self):
        """Logica per generare il report Recheck."""
        # Estrazione e calcolo dei dati
        vapt_data, recheck_data = get_vuln_data_for_vapt_and_recheck(self.mongo_data)
        vapt_counts, recheck_counts, categories = get_vuln_data_for_vapt_and_recheck_by_category(self.mongo_data)
        vapt_name_counts, recheck_name_counts, all_names = get_vuln_data_for_vapt_and_recheck_by_name(self.mongo_data)
        
        # Creazione dei grafici specifici per Recheck
        self.recheck.create_recheck_summary(list(vapt_data.values()), list(recheck_data.values()), os.path.join(self.graph_dir, 'recheck_summary.png'))         
        self.recheck.create_vapt_recheck_summary(list(vapt_data.values()), list(recheck_data.values()), os.path.join(self.graph_dir, 'vapt_recheck_summary.png'))         
        self.recheck.create_vapt_recheck_histogram(vapt_counts, recheck_counts, categories, os.path.join(self.graph_dir, 'vapt_recheck_histogram.png')) 
        self.recheck.create_histogram_vuln_by_name(all_names, vapt_name_counts, all_names, recheck_name_counts, os.path.join(self.graph_dir, 'vuln_histogram_by_name.png'))

        # Modifica del documento Word
        mt = ModificaTemplate(
            self.template_path, 
            self.output_path,
            self.graph_dir,
            )
        mt.modify_word_document_with_charts(self.mongo_data)


if __name__ == '__main__':
    # Esempio di utilizzo della classe GeneralReport per generare report VAPT e Recheck
    report_generator_dashboard = GeneralReport()
    report_generator_dashboard.set_template('dashboard.docx', 'output_report_dashboard.docx')
    report_generator_dashboard.run_vapt()
    
    report_generator_recheck = GeneralReport()
    report_generator_recheck.set_template('recheck.docx', 'output_report_recheck.docx')
    report_generator_recheck.run_recheck()
