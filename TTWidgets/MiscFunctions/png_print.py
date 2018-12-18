'''
This script is used to print pngs to the system's default printer.
'''

import win32print
import win32ui
from PIL import Image, ImageWin, ImageChops

def print_png(file_name):
    '''
    This function takes in a png file name 
    and physically prints the image.
    '''
    # Constants for GetDeviceCaps
    HORZRES = 8
    VERTRES = 10

    # LOGPIXELS = dots per inch
    ###LOGPIXELSX = 88
    ###LOGPIXELSY = 90

    # PHYSICALWIDTH/PHYSICALHEIGHT = total area
    PHYSICALWIDTH = 110
    PHYSICALHEIGHT = 111

    # PHYSICALOFFSETX/PHYSICALOFFSETY = left / top margin
    ###PHYSICALOFFSETX = 112
    ###PHYSICALOFFSETY = 113

    printer_name = win32print.GetDefaultPrinter()

    # You can only write a Device-independent bitmap
    #  directly to a Windows device context; therefore
    #  we need (for ease) to use the Python Imaging
    #  Library to manipulate the image.
    #
    # Create a device context from a named printer
    #  and assess the printable size of the paper.
    png_printer_DC = win32ui.CreateDC()
    png_printer_DC.CreatePrinterDC(printer_name)
    printable_area = png_printer_DC.GetDeviceCaps(HORZRES), png_printer_DC.GetDeviceCaps(VERTRES)
    printer_size = png_printer_DC.GetDeviceCaps(PHYSICALWIDTH), png_printer_DC.GetDeviceCaps(PHYSICALHEIGHT)
    ###printer_margins = png_printer_DC.GetDeviceCaps(PHYSICALOFFSETX), png_printer_DC.GetDeviceCaps(PHYSICALOFFSETY)

    # Open the image, rotate it if it's wider than
    #  it is high, and work out how much to multiply
    #  each pixel by to get it as big as possible on
    #  the page without distorting.
    bmp = Image.open(file_name)
    bmp.show()
    if bmp.size[0] > bmp.size[1]:
        bmp = bmp.rotate(90)
    
    ratios = [0.9 * printable_area[0] / bmp.size[0], 0.9 * printable_area[1] / bmp.size[1]]
    scale = min(ratios)

    # Start the print job, and draw the bitmap to
    #  the printer device at the scaled size.
    png_printer_DC.StartDoc(file_name)
    png_printer_DC.StartPage()

    dib = ImageWin.Dib(bmp)
    scaled_width, scaled_height = [int(scale * i) for i in bmp.size]
    x1 = int((printer_size[0] - scaled_width) / 2)
    y1 = int((printer_size[1] - scaled_height) / 2)
    x2 = x1 + scaled_width
    y2 = y1 + scaled_height
    dib.draw(png_printer_DC.GetHandleOutput(), (x1, y1, x2, y2))

    png_printer_DC.EndPage()
    png_printer_DC.EndDoc()
    png_printer_DC.DeleteDC()
