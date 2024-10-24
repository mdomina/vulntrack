from docx import Document
from docx.shared import Inches
from DrawGraphs import DrawGraphs
from DrawGraphs import Recheck  # Importa la classe Recheck
import os

# Inizializza la classe DrawGraphs
draw_graphs = DrawGraphs()

# Inizializza la classe Recheck
recheck = Recheck()

output_dir = 'output'
graph_dir = 'grafici'

if not os.path.exists(graph_dir):
    os.makedirs(graph_dir)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

template_dir = 'template'

if not os.path.exists(template_dir):
    os.makedirs(template_dir)

# Funzione per sostituire i tag nel documento Word
def replace_tag_with_chart(doc, tag, image_path, image_width=Inches(5)):
    for paragraph in doc.paragraphs:
        if tag in paragraph.text:
            paragraph.text = ''
            paragraph.add_run().add_picture(image_path, width=image_width)

def replace_tag_with_donut_charts(doc, tag):
    for paragraph in doc.paragraphs:
        if tag in paragraph.text:
            # Trova il paragrafo con il tag e rimuovi il tag
            paragraph.text = paragraph.text.replace(tag, '')

            # Crea una tabella con 1 riga e 4 colonne per i grafici a ciambella
            table = doc.add_table(rows=1, cols=4)

            # Inserisci ogni grafico a ciambella in una cella della tabella
            row_cells = table.rows[0].cells
            row_cells[0].paragraphs[0].add_run().add_picture(os.path.join(graph_dir, 'critiche.png'), width=Inches(1.5))
            row_cells[1].paragraphs[0].add_run().add_picture(os.path.join(graph_dir, 'alte.png'), width=Inches(1.5))
            row_cells[2].paragraphs[0].add_run().add_picture(os.path.join(graph_dir, 'medie.png'), width=Inches(1.5))
            row_cells[3].paragraphs[0].add_run().add_picture(os.path.join(graph_dir, 'basse.png'), width=Inches(1.5))
            
            paragraph._element.addnext(table._element)

# Funzione per leggere e modificare un documento Word esistente
def modify_word_document_with_charts(input_doc_path, output_doc_path):
    doc = Document(input_doc_path)

    # Genera i grafici usando la classe DrawGraphs
    draw_graphs.create_bar_chart()
    draw_graphs.create_timeline_chart()
    draw_graphs.create_pie_chart()
    draw_graphs.create_horizontal_bar_chart()
    draw_graphs.create_bar_chart_by_name()
    draw_graphs.create_all_donut_charts()
    draw_graphs.create_bar_chart_by_category()

    # Genera il grafico di riepilogo Recheck usando la classe Recheck
    data_vapt = [0, 0, 11, 6]  # Dati per VAPT
    data_recheck = [0, 0, 2, 3]  # Dati per Recheck
    data_vapt_tipologia = [4, 1, 2, 4, 6]
    data_recheck_tipologia = [2, 0, 1, 2, 4]
    categories = ['Security Misconfiguration', 'Identification', 'Cryptographic Failures', 'Injection', 'Insecure Design']

    labels_vapt = ['Software Information Disclosure', 'SQL Injection', 'Weak Password Requirements', 'Cross-Site Scripting', 'Buffer Overflow']
    sizes_vapt = [12, 9, 7, 6, 4]

    labels_recheck = ['Buffer Overflow', 'Cross-Site Scripting', 'SQL Injection', 'Weak Password Requirements']
    sizes_recheck = [10, 8, 6, 4]

    recheck.create_recheck_summary(data_vapt, data_recheck, 'recheck_summary.png')
    recheck.create_vapt_recheck_summary(data_vapt, data_recheck, 'vapt_recheck_summary.png')
    recheck.create_vapt_recheck_histogram(data_vapt_tipologia, data_recheck_tipologia, categories, 'vapt_recheck_histogram.png')
    recheck.create_histogram_vuln_by_name(labels_vapt, sizes_vapt, labels_recheck, sizes_recheck, 'vuln_histogram_by_name.png')

    # Sostituisci i tag con i grafici
    replace_tag_with_chart(doc, '{{tag_graficotimeline}}', os.path.join(graph_dir, 'timeline_chart.png'))
    replace_tag_with_chart(doc, '{{tag_complessive}}', os.path.join(graph_dir, 'pie_chart.png'))
    replace_tag_with_chart(doc, '{{tag_mensili}}', os.path.join(graph_dir, 'horizontal_bar_chart.png'))
    replace_tag_with_chart(doc, '{{tag_name}}', os.path.join(graph_dir, 'bar_chart_by_name.png'))
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

modify_word_document_with_charts(file_template_dashboard, file_output_dashboard)
modify_word_document_with_charts(file_template_recheck, file_output_recheck)

