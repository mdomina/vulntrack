from docx import Document
from docx.shared import Inches
from DrawGraphs import DrawGraphs
import os
# Inizializza la classe DrawGraphs
draw_graphs = DrawGraphs()
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
            if tag in paragraph.text:
                paragraph.text = paragraph.text.replace(tag, '')

                # Crea una tabella con 1 riga e 4 colonne per i grafici a ciambella
                table = doc.add_table(rows=1, cols=4)

                # Inserisci ogni grafico a ciambella in una cella della tabella
                row_cells = table.rows[0].cells
                row_cells[0].paragraphs[0].add_run().add_picture(os.path.join(graph_dir, 'critiche.png'), width=Inches(1.5))
                row_cells[1].paragraphs[0].add_run().add_picture(os.path.join(graph_dir, 'alte.png'), width=Inches(1.5))
                row_cells[2].paragraphs[0].add_run().add_picture(os.path.join(graph_dir, 'medie.png'), width=Inches(1.5))
                row_cells[3].paragraphs[0].add_run().add_picture(os.path.join(graph_dir, 'basse.png'), width=Inches(1.5))

                # Aggiungi la tabella subito dopo il paragrafo corrente
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

    # Sostituisci i tag con i grafici
    replace_tag_with_chart(doc, '{{tag_graficotimeline}}', os.path.join(graph_dir, 'timeline_chart.png'))
    replace_tag_with_chart(doc, '{{tag_complessive}}', os.path.join(graph_dir, 'pie_chart.png'))
    replace_tag_with_chart(doc, '{{tag_mensili}}', os.path.join(graph_dir, 'horizontal_bar_chart.png'))
    replace_tag_with_chart(doc, '{{tag_name}}', os.path.join(graph_dir, 'bar_chart_by_name.png'))
    replace_tag_with_chart(doc, '{{tag_categoria}}', os.path.join(graph_dir, 'bar_chart_by_category.png'))

    replace_tag_with_donut_charts(doc, '{{tag_grafici_donut}}')

    # Salva il documento modificato
    doc.save(output_doc_path)

# Esecuzione del codice per modificare il documento con i grafici
file_template = os.path.join(template_dir, 'ARIA_vulntrak.docx')
file_output = os.path.join(output_dir, 'output_report.docx')


modify_word_document_with_charts(file_template, file_output)
