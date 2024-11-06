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
        self.doc = Document(self.template)
        self.temp_docx_path = "temp_modified_document.docx"

    def replace_tags_with_charts_column(self, tag: str, saved_charts: list):
        """
        Sostituisce un tag nel documento con una serie di immagini di grafici disposte in colonna.
        Ogni grafico della lista `saved_charts` viene inserito uno sotto l'altro in una singola colonna.

        :param tag: Il tag nel documento Word che indica dove inserire i grafici.
        :param saved_charts: Lista dei percorsi dei file dei grafici da inserire nel documento.
        """
        # Calcola la larghezza della pagina meno i margini
        section = self.doc.sections[0]
        page_width = section.page_width
        margin_left = section.left_margin
        margin_right = section.right_margin
        available_width = page_width - margin_left - margin_right

        # Trova il paragrafo contenente il tag e inserisce i grafici in colonna
        for paragraph in self.doc.paragraphs:
            if tag in paragraph.text:
                paragraph.text = ''  # Svuota il paragrafo per inserirvi le immagini
                
                for chart_path in saved_charts:
                    run = paragraph.add_run()
                    # Aggiunge ciascun grafico con la larghezza adattata alla pagina
                    run.add_picture(chart_path, width=available_width)
                    
                    # Aggiunge uno spazio per separare i grafici, mantenendo una colonna
                    paragraph = self.doc.add_paragraph()

        # Salva il documento modificato come file temporaneo
        self.doc.save(self.temp_docx_path)

    def replace_tag_with_chart(self, tag: str, image_path: str):
        """
        Sostituisce un tag nel documento con un'immagine del grafico, adattando la larghezza
        dell'immagine alla larghezza della pagina meno i margini.
        """
        # Calcola la larghezza della pagina meno i margini
        section = self.doc.sections[0]
        page_width = section.page_width
        margin_left = section.left_margin
        margin_right = section.right_margin
        available_width = page_width - margin_left - margin_right

        # Sostituisci il tag con l'immagine ridimensionata
        for paragraph in self.doc.paragraphs:
            if tag in paragraph.text:
                paragraph.text = ''
                # Imposta la larghezza dell'immagine in modo che occupi tutta la larghezza disponibile
                paragraph.add_run().add_picture(image_path, width=available_width)
        
        # Salva il documento modificato come file temporaneo
        self.doc.save(self.temp_docx_path)
 
    def replace_tag_with_donut_charts(self, tag:str):
        """Sostituisce un tag con una tabella contenente i grafici a ciambella."""
        for paragraph in self.doc.paragraphs:
            if tag in paragraph.text:
                paragraph.text = paragraph.text.replace(tag, '')

                table = self.doc.add_table(rows=1, cols=4)
                row_cells = table.rows[0].cells
                row_cells[0].paragraphs[0].add_run().add_picture(os.path.join(self.graph_dir,'critical.png'), width=Inches(1.5))                
                row_cells[1].paragraphs[0].add_run().add_picture(os.path.join(self.graph_dir,'high.png'), width=Inches(1.5))                 
                row_cells[2].paragraphs[0].add_run().add_picture(os.path.join(self.graph_dir,'medium.png'), width=Inches(1.5))                 
                row_cells[3].paragraphs[0].add_run().add_picture(os.path.join(self.graph_dir,'low.png'), width=Inches(1.5))
                paragraph._element.addnext(table._element)

    def modify_word_document_with_charts(self, mongo_data:list[dict]):
        """Modifica un documento Word inserendo i grafici generati."""

        # Determina se il tipo di audit è Recheck o VAPT
        is_recheck = any(item.get('auditType', '').lower() == 'recheck' for item in mongo_data)
        pie_chart_name = 'pie_chart_recheck.png' if is_recheck else 'pie_chart_vapt.png'

        # Sostituisce i tag con i grafici specifici
        # self.replace_tag_with_chart('{{tag_complessive}}', os.path.join(self.graph_dir, pie_chart_name))
        # self.replace_tag_with_chart('{{tag_mensili}}', os.path.join(self.graph_dir, 'horizontal_bar_chart.png'))
        # self.replace_tag_with_chart('{{tag_name}}', os.path.join(self.graph_dir, 'horizontal_bar_chart_by_name.png'))
        # self.replace_tag_with_chart('{{tag_categoria}}', os.path.join(self.graph_dir, 'bar_chart_by_category.png'))

        # # Grafici per il riepilogo Recheck
        # self.replace_tag_with_chart('{{tag_recheck_summary}}', os.path.join(self.graph_dir, 'recheck_summary.png'))
        # self.replace_tag_with_chart('{{tag_vapt_recheck}}', os.path.join(self.graph_dir, 'vapt_recheck_summary.png'))
        # self.replace_tag_with_chart('{{tag_vapt_recheck_histogram}}', os.path.join(self.graph_dir, 'vapt_recheck_histogram.png'))
        # self.replace_tag_with_chart('{{tag_vuln_by_name}}', os.path.join(self.graph_dir, 'vuln_histogram_by_name.png'))

        # # Inserimento dei grafici a ciambella (donut charts)
        # self.replace_tag_with_donut_charts('{{tag_grafici_donut}}')

        

        # Converte il documento modificato in PDF usando LibreOffice
        subprocess.run([
            '/usr/bin/libreoffice', '--headless', '--convert-to', 'pdf',
            self.temp_docx_path, '--outdir', os.path.dirname(self.output)
        ])

        # Rinomina il file PDF generato da LibreOffice nella destinazione desiderata
        temp_pdf_path = os.path.splitext(self.temp_docx_path)[0] + ".pdf"
        temp_pdf_path = os.path.join(os.path.dirname(self.output), temp_pdf_path)

        if os.path.exists(temp_pdf_path):
            os.rename(temp_pdf_path, self.output)
        else:
            raise FileNotFoundError("Conversione fallita, il file PDF non è stato generato.")

        # Rimuove il file temporaneo .docx
        os.remove(self.temp_docx_path)