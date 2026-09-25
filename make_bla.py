import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib import colors
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Ett anpassat system för att räkna sidor dynamiskt och lägga till sidhuvud/sidfot"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#666666"))
        
        # Rita sidhuvud (Undantag för första sidan med registret)
        if self._pageNumber > 1:
            self.drawString(54, 750, "BLA BLA BLA — CONTINUOUS STREAM SYSTEM")
            self.setStrokeColor(colors.HexColor("#E0E0E0"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
        
        # Rita sidfot på alla sidor
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 40, page_text)

def generate_bla_pdf(filename="bla_stream_document.pdf"):
    # Skapa dokumentets grundstruktur med 2 cm marginaler
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54, rightMargin=54,
        topMargin=72, bottomMargin=72
    )
    
    styles = getSampleStyleSheet()
    
    # Skapa egna stilar för att kontrollera textmassan exakt
    title_style = ParagraphStyle('RegTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=20, leading=24, alignment=TA_CENTER, spaceAfter=20)
    h1_style = ParagraphStyle('CustomH1', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=14, leading=18, spaceBefore=15, spaceAfter=10, keepWithNext=True)
    body_style = ParagraphStyle('BlaBody', parent=styles['BodyText'], fontName='Helvetica', fontSize=10, leading=14, alignment=TA_JUSTIFY, spaceAfter=12)
    ledger_style = ParagraphStyle('LedgerText', fontName='Helvetica', fontSize=10, leading=12)
    ledger_bold = ParagraphStyle('LedgerBold', fontName='Helvetica-Bold', fontSize=10, leading=12)

    story = []
    
    # 1. BYGG NAVIGATIONSREGISTER (SIDA 1)
    story.append(Paragraph("DOCUMENT NAVIGATION LEDGER", title_style))
    story.append(Spacer(1, 15))
    
    # Skapa matrisdata för de 10 segmenten (beräknat utifrån textmängden)
    table_data = [[Paragraph("Segment Identifier", ledger_bold), Paragraph("Content Matrix", ledger_bold), Paragraph("Estimated Target Page", ledger_bold)]]
    
    page_tracker = 2
    for i in range(1, 11):
        table_data.append([
            Paragraph(f"SEGMENT-0{i}", ledger_style),
            Paragraph("Continuous stream of 'bla' iteration matrix", ledger_style),
            Paragraph(f"Page {page_tracker}", ledger_style)
        ])
        page_tracker += 20  # Varje segment fyller ca 20 sidor
        
    nav_table = Table(table_data, colWidths=[120, 260, 124])
    nav_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F2F2F2")),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D0D0D0")),
    ]))
    story.append(nav_table)
    story.append(PageBreak()) # Tvinga fram sidbrytning till textströmmen
    
    # 2. GENERERA TEXTSTRÖMMEN (SIDA 2 TILL 200+)
    # Bygg en massiv blockjusterad textmassa av ordet "bla"
    bla_chunk = " ".join(["bla"] * 480) + "." # Ungefär en boksida per stycke
    
    for segment in range(1, 11):
        story.append(Paragraph(f"SEGMENT {segment}: THE INHERENT CONTINUUM", h1_style))
        story.append(Spacer(1, 10))
        
        # Fyll varje segment med tillräckligt många stycken för att generera ca 20 sidor
        for paragraph_count in range(20):
            story.append(Paragraph(bla_chunk, body_style))
            
        if segment < 10:
            story.append(PageBreak())
            
    # Kompilera och generera PDF-filen
    doc.build(story, canvasmaker=NumberedCanvas)

if __name__ == "__main__":
    generate_bla_pdf()
