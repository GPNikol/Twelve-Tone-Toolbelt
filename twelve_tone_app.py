'''
This script provides a GUI interface for a Twelve Tone Matrix.

It has been adapted from a previous - terminal based application
to work as a Python Kivy Application.
'''
import kivy
import kivy.uix.settings
kivy.require('1.10.1')

from toolbar_widget import ToolBarWidget
from matrixtools_widget import MatrixTools
from matrix_widget import MatrixWidget

from kivy.app import App
from kivy.logger import Logger
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label

class RootWidget(FloatLayout):
    '''
    This widget holds the rest of the widgets and 
    the functions for interactions between them.
    '''
    def __init__(self, **kwargs):
        '''
        Initializes the primary application layout,
        the parent to all the other layouts.
        Holds the prime row for user's to fill in
        '''
        super(RootWidget, self).__init__(**kwargs)
        self.error_pop_set = Popup(title="PRIME ROW ERROR",
                            content=Label(text='''RULES FOR A PRIME ROW:
                                                \n -Must contain all numbers zero through eleven
                                                \n -Must contain each only once''',
                                        font_size=self.height/6),
                            size_hint=(None,None),
                            size=(600,400))
        self.my_mat = self.ids.matrix
        self.prime = self.ids.prime_row
        self.my_tools = self.ids.matrix_tools
        self.tool_bar = self.ids.tools

        #Binding functions to settings drop down menu
        file_dropdown = DropDown()
        btn_names = ['Save', 'Print', 'Print Options', 'Properties']
        for indx in range(4):
            btn = Button(text=f'{btn_names[indx]}', size_hint=(None, None), width=self.width, height=40)
            btn.bind(on_press=lambda btn: file_dropdown.select(btn.text))
            file_dropdown.add_widget(btn)
        self.tool_bar.children[0].bind(on_release=file_dropdown.open)
        file_dropdown.bind(on_select=lambda instance, x: setattr(self.tool_bar.children[0], 'text', x))

        #Binds functions directly effecting the matrix to their buttons
        self.my_tools.children[4].bind(on_press=lambda *args: self.build_matrix(self.prime, self.my_mat))
        self.my_tools.children[3].bind(on_press=lambda *args: self.clear_matrix(self.prime, self.my_mat))
        self.my_tools.children[2].children[1].bind(on_press=lambda *args: self.flip_matrix(self.my_mat, MatrixWidget.FLAT_ALPHA_REP))
        self.my_tools.children[2].children[0].bind(on_press=lambda *args: self.flip_matrix(self.my_mat, MatrixWidget.SHARP_ALPHA_REP))
        self.my_tools.children[1].children[1].bind(on_press=lambda *args: self.flip_matrix(self.my_mat, MatrixWidget.EXPAND))
        self.my_tools.children[1].children[0].bind(on_press=lambda *args: self.flip_matrix(self.my_mat, MatrixWidget.ALPHANUM_REP))
        self.my_tools.children[0].bind(on_press=lambda *args: self.flip_matrix(self.my_mat, MatrixWidget.DEFAULT))

        #Binds text inputs to labels
        for col in range(12):
            txt_in = self.prime.children[11 - col]
            lbl = self.my_mat.children[self.my_mat.translate_coords(0,col)]
            txt_in.bind(text=lbl.setter('text'))

    def _convert_prime_row(self, row):
        '''
        Converts a string list to a numerical list, reverses it, and returns it.
        '''
        tmp = [] #temporary list to operate on the prime row

        #Convert Prime row to integers for easier calculations
        for child in row.children:
            if child.text != '': 
                tmp.append(int(child.text))

        tmp.reverse() #Compensates for the FIFO method kivy uses to load widgets. 
        return tmp

    def _flip_back(self, mat, rep):
        '''
        Returns the matrix to numerical representation.
        '''
        for row in range(12):
            for col in range(12):
                r_tmp = rep.index(mat.children[mat.translate_coords(row, col)].text)
                mat.children[mat.translate_coords(row, col)].text = str(r_tmp)

    def _expand_matrix(self, mat):
        '''
        Expands the matrix to show the musical distance between notes.
        '''
        #Creates a copy of the original matrix
        original_mat = ['' for i in range(144)]
        for t_row in range(12):
            for t_col in range(12):
                original_mat[mat.translate_coords(t_row, t_col)] = int(mat.children[mat.translate_coords(t_row, t_col)].text)

        for row in range(12):
            #Variables to keep track of the number of regressions in each row and column
            horizontal_twelves = 0
            vertical_twelves = 0

            for col in range(12):
                #Skips an iteration for the matrix's diagonal
                if row == col:
                    continue
                #Applies to every value outside the diagonal
                elif col > row:
                    #Adds 12 to every value that regresses in the original row
                    current_val_h = original_mat[mat.translate_coords(row, col)]
                    previous_val_h = original_mat[mat.translate_coords(row, col-1)]
                    if current_val_h < previous_val_h:
                        horizontal_twelves += 1
                    new_val_h = current_val_h + (12 * horizontal_twelves)
                    mat.children[mat.translate_coords(row, col)].text = str(new_val_h)

                    #Adds 12 to every value that regresses in the original column
                    current_val_v = original_mat[mat.translate_coords(col, row)]
                    previous_val_v = original_mat[mat.translate_coords(col-1, row)]
                    if current_val_v < previous_val_v:
                        vertical_twelves += 1
                    new_val_v = current_val_v + (12 * vertical_twelves)
                    mat.children[mat.translate_coords(col, row)].text = str(new_val_v)

    def _contract_matrix(self, mat):
        '''
        Converts the matrix back to default from the expanded variant
        '''
        for row in range(12):
            for col in range(12):
                i_tmp = int(mat.children[mat.translate_coords(row, col)].text) % 12
                mat.children[mat.translate_coords(row, col)].text = str(i_tmp)

    def build_matrix(self, p_row, mat):
        '''
        Builds the rest of the matrix outside the prime row
        '''
        tmp = self._convert_prime_row(p_row)

        #The set from the prime row must have the same contents as the row below.
        if set(tmp) != set(range(12)):
            self.error_pop_set.open()
        #If the above two conditions are met then the rest of the matrix can be filled.
        else:
            intervals = [(tmp[x] - tmp[x-1]) % 12 for x in range(1, 12) if tmp[x] != '']

            #Use Twelve Tone algorithm to construst the full matrix.
            for row in range(1, len(intervals)+1):
                for col in range(len(intervals)+1):
                    val = int(mat.children[mat.translate_coords(row-1, col)].text)
                    #(row, col) = ((row - 1, col) - ((0, col) - (0, col - 1)) % 12) % 12
                    mat.children[mat.translate_coords(row, col)].text = str((val - intervals[row-1]) % 12)

    def clear_matrix(self, row, mat):
        '''
        Clears the prime row and matrix of all content
        '''
        for item in row.children:
            item.text = ''
        for cell in mat.children:
            cell.text = ''

    def flip_matrix(self, mat, rep):
        '''
        POSSIBLE REPRESENTATIONS: ALPHANUM_REP, FLAT_ALPHA_REP, SHARP_ALPHA_REP, EXPAND

        Changes the representation of the matrix to another.
        '''
        try:
            tmp_h = [mat.children[mat.translate_coords(0, col)].text for col in range(12)]
            tmp_v = [mat.children[mat.translate_coords(col, 0)].text for col in range(12)]

            #If the matrix is in numeral representation proceed to flip to new rep
            if set(tmp_h) == set(map(str,range(12))) and set(tmp_v) == set(map(str,range(12))) and rep != MatrixWidget.DEFAULT:
                if rep == MatrixWidget.EXPAND:
                    self._expand_matrix(mat)
                else:
                    #Iterate through the matrix, altering the representation
                    for row in range(12):
                        for col in range(12):
                            r_tmp = rep[int(mat.children[mat.translate_coords(row, col)].text)]
                            mat.children[mat.translate_coords(row, col)].text = str(r_tmp)
            #Make sure there's a matrix to operate on
            elif len(tmp_h) != 12:
                self.error_pop_set.open()
            #If the matrix isn't in numeral representation flip back to it then proceed
            else:
                if set(tmp_h) == set(MatrixWidget.ALPHANUM_REP):
                    self._flip_back(mat, MatrixWidget.ALPHANUM_REP)
                elif set(tmp_h) == set(MatrixWidget.FLAT_ALPHA_REP):
                    self._flip_back(mat, MatrixWidget.FLAT_ALPHA_REP)
                elif set(tmp_h) == set(MatrixWidget.SHARP_ALPHA_REP):
                    self._flip_back(mat, MatrixWidget.SHARP_ALPHA_REP)
                else:
                    self._contract_matrix(mat)
                if rep != MatrixWidget.DEFAULT:
                    self.flip_matrix(mat, rep)
        except:
            self.error_pop_set.open()

class TwelveToneApp(App):
    '''
    This class inherits from kivy's app class.
    This is where the application's life cycle begins.
    '''
    def build(self):
        '''
        This method contains some items that need to
        be used and initialized in the app.
        '''
        self.myapp = RootWidget()
        return self.myapp
    
    def on_stop(self):
        '''
        Tests for safe close.
        This will likely contain more function later as the app evolves.
        '''
        Logger.critical('Goodbye!')

if __name__ == "__main__":
    TwelveToneApp().run()