from loguru import logger
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

Y_BOTTOM_MARGIN = 50
Y_TOP_MARGIN = 50
LINE_SIZE = 10
PARAGRAPHS_DISTANCE = 30

def register_monospaced_font(font_path):
    pdfmetrics.registerFont(TTFont('Courier', font_path))

def set_monospaced_font(canvas):
    canvas.setFont("Courier", LINE_SIZE)

def generate(input_file_path, output_file_path):

    # Register the monospaced font
    font_path = "./FreeMono.ttf"  # Replace with the path to your monospaced font file
    register_monospaced_font(font_path)

    # Create a PDF file
    pdf_file_path = output_file_path + ".pdf"
    c = canvas.Canvas(pdf_file_path, pagesize=A4)

    # Calculate the margins
    left_margin = 50
    right_margin = A4[0] - 50

    # Read text content from the input file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text_content = file.read()

    # Split text content into paragraphs and draw on PDF
    paragraphs = text_content.split('\n\n')  # Split by blank lines to identify paragraphs
    logger.info(f'We have identified {len(paragraphs)} paragraphs:')
    # print(paragraphs)
    y_position = A4[1] - Y_TOP_MARGIN  # Starting position from the top of the page
    set_monospaced_font(c)
    for paragraph in paragraphs:
        lines = paragraph.split('\n')
        
        paragraph_size = len(lines)
        if (y_position - (paragraph_size*LINE_SIZE)) <= Y_BOTTOM_MARGIN:    
            # Start a new page when reaching the bottom
            c.showPage()
            set_monospaced_font(c)  # Set monospaced font for the new page
            y_position = A4[1] - Y_TOP_MARGIN  # Reset Y position for the new page
        for line in lines:
            # Calculate the x-coordinate based on left margin
            x_position = left_margin
            c.drawString(x_position, y_position, line)
            y_position -= LINE_SIZE  # Adjust the vertical position for the next line (using a smaller value for Courier font)

        # Add some space between paragraphs
        y_position -= PARAGRAPHS_DISTANCE

    c.save()

    logger.success(f"PDF file created: {pdf_file_path}")