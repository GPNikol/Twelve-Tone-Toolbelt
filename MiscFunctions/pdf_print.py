from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

import cgi
import tempfile
import win32api

def convert_to_pdf(src_file_name):
    '''
    Uses reportlab to convert a standard text file to a pdf doc for
    reliable printing of large documents.
    '''
    pdf_file_name = tempfile.mktemp(".pdf")

    styles = getSampleStyleSheet()
    h1 = styles['h1']
    normal = styles["Normal"]

    doc = SimpleDocTemplate(pdf_file_name)
    #
    # reportlab expects to see XML-compliant
    #  data; need to escape ampersands &c.
    #
    text = cgi.escape(open (src_file_name).read()).splitlines()

    #
    # Take the first line of the document as a
    #  header; the rest are treated as body text.
    #
    story = [Paragraph('', h1)]
    for line in text:
        story.append(Paragraph(line, normal))
        story.append(Spacer(1, 0.2 * inch))

    doc.build(story)
    win32api.ShellExecute(0, "print", pdf_file_name, None, ".", 0)

def main():
    convert_to_pdf("test.txt")

if __name__ == '__main__':
    main()
