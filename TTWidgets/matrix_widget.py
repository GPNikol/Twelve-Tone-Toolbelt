'''
CREATED BY: Gregory P. Nikol
MOST RECENT UPDATE: December 14, 2018

Class for creating and acting on a 12x12 matrix in kivy. 
'''
import kivy
kivy.require('1.10.1')

from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

class MatrixCell(Label):
    '''
    This widget is a predesigned label to be used repeatedly by the matrix widget.
    '''
    pass

class MatrixWidget(GridLayout):
    '''
    This widget contains the matrix cells and further functions for operations on the matrix.
    Also contains different representations of the contents of a Twelvetone matrix:
    ALPHANUM_REP: 10 and 11 are "t" and "e" respectively. 
    FLAT_ALPHA_REP: All values become their corresponding musical notation (with flats)
    SHARP_ALPHA_REP: All values become their corresponding musical notation (with sharps)
    DEFAULT = Simply acts as a flat to revent back to numerical representation
    EXPAND = Simply acts as a flat to trigger an algorithm to run over the values in the matrix
    '''
    ALPHANUM_REP = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 't', 'e']
    FLAT_ALPHA_REP = ['C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B']
    SHARP_ALPHA_REP = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    DEFAULT = "default"
    EXPAND = "expand"

    def __init__(self, **kwargs):
        '''
        Initializes the matrix for the application
        '''
        super(MatrixWidget, self).__init__(**kwargs)
        cell = 0
        while cell < 144:
            mat_cell = MatrixCell(color=[0,0,0,1])
            self.add_widget(mat_cell)
            cell+=1

        #Test for retreiving widgets
        #print(self.children[self.translate_coords(10, 5)].text)
        #self.children[self.translate_coords(1,7)].text = str(self.translate_coords(1,7))

    def translate_coords(self, row, col):
        '''
        Used to retrieve the values from the correct coordinates.
        Compensates for kivy's backward loading of widgets.
        '''
        return (11 - row) * 12 + (11 - col)
