from docx import Document
from docx.document import Document as DocumentObject
import os
import subprocess
from app.utility.report_creation.crea_grafici import Dashboard
from docx.shared import Inches

class ModificaTemplate:
    def __init__(self, template_path:str, output_doc_path:str, graph_dir:str) -> None:
        self.vapt_graphs = Dashboard()
        self.template = template_path # percorso del template in World
        self.output = output_doc_path # percorso di destinazione una volta modificato il template
        self.graph_dir = graph_dir # percorso della directory dei grafici
    
    # def replace_tag_with_chart(self, doc:DocumentObject, tag:str, image_path:str, image_width=Inches(5)):
    #     """Sostituisce un tag nel documento con un'immagine del grafico."""
    #     for paragraph in doc.paragraphs:
    #         if tag in paragraph.text:
    #             paragraph.text = ''
    #             paragraph.add_run().add_picture(image_path, width=image_width)

    def replace_tag_with_chart(self, doc: DocumentObject, tag: str, image_path: str):
        """
        Sostituisce un tag nel documento con un'immagine del grafico, adattando la larghezza
        dell'immagine alla larghezza della pagina meno i margini.
        """
        # Calcola la larghezza della pagina meno i margini
        section = doc.sections[0]
        page_width = section.page_width
        margin_left = section.left_margin
        margin_right = section.right_margin
        available_width = page_width - margin_left - margin_right

        # Sostituisci il tag con l'immagine ridimensionata
        for paragraph in doc.paragraphs:
            if tag in paragraph.text:
                paragraph.text = ''
                # Imposta la larghezza dell'immagine in modo che occupi tutta la larghezza disponibile
                paragraph.add_run().add_picture(image_path, width=available_width)

    
    def replace_tag_with_donut_charts(self, doc:DocumentObject, tag:str):
        """Sostituisce un tag con una tabella contenente i grafici a ciambella."""
        for paragraph in doc.paragraphs:
            if tag in paragraph.text:
                paragraph.text = paragraph.text.replace(tag, '')

                table = doc.add_table(rows=1, cols=4)
                row_cells = table.rows[0].cells
                row_cells[0].paragraphs[0].add_run().add_picture(os.path.join(self.graph_dir,'critical.png'), width=Inches(1.5))                
                row_cells[1].paragraphs[0].add_run().add_picture(os.path.join(self.graph_dir,'high.png'), width=Inches(1.5))                 
                row_cells[2].paragraphs[0].add_run().add_picture(os.path.join(self.graph_dir,'medium.png'), width=Inches(1.5))                 
                row_cells[3].paragraphs[0].add_run().add_picture(os.path.join(self.graph_dir,'low.png'), width=Inches(1.5))
                paragraph._element.addnext(table._element)

    def modify_word_document_with_charts(self, mongo_data:list[dict]):
        """Modifica un documento Word inserendo i grafici generati."""
        doc = Document(self.template)

        # Determina se il tipo di audit è Recheck o VAPT
        is_recheck = any(item.get('auditType', '').lower() == 'recheck' for item in mongo_data)
        pie_chart_name = 'pie_chart_recheck.png' if is_recheck else 'pie_chart_vapt.png'

        # Sostituisce i tag con i grafici specifici
        self.replace_tag_with_chart(doc, '{{tag_complessive}}', os.path.join(self.graph_dir, pie_chart_name))
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

        # Salva il documento modificato come file temporaneo
        temp_docx_path = "temp_modified_document.docx"
        doc.save(temp_docx_path)

        # Converte il documento modificato in PDF usando LibreOffice
        subprocess.run([
            '/usr/bin/libreoffice', '--headless', '--convert-to', 'pdf',
            temp_docx_path, '--outdir', os.path.dirname(self.output)
        ])

        # Rinomina il file PDF generato da LibreOffice nella destinazione desiderata
        temp_pdf_path = os.path.splitext(temp_docx_path)[0] + ".pdf"
        temp_pdf_path = os.path.join(os.path.dirname(self.output), temp_pdf_path)

        if os.path.exists(temp_pdf_path):
            os.rename(temp_pdf_path, self.output)
        else:
            raise FileNotFoundError("Conversione fallita, il file PDF non è stato generato.")

        # Rimuove il file temporaneo .docx
        os.remove(temp_docx_path)