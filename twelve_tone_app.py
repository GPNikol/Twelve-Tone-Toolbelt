'''
This script provides a GUI interface for a Twelve Tone Matrix.

It has been adapted from a previous - terminal based application
to work as a Python Kivy Application.
'''
import kivy
import kivy.properties
import kivy.graphics.vertex_instructions
import kivy.graphics.context_instructions
import kivy.uix.settings
kivy.require('1.10.1')

from math import floor
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.logger import Logger

Builder.load_string('''
<TextInput>:
    font_name: 'DejaVuSans'

<Label>:
    font_name: 'DejaVuSans'

<MatrixCell>
    font_size: self.height * .5
    canvas.before:
        Color:
            rgba: 0, 0, 0, 1
        Rectangle:
            pos: self.pos
            size: self.width * 1.05, self.height * 1.05
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.width, self.height

<ToolBarWidget>
    anchor_x: 'center'
    anchor_y: 'center'

<MatrixTools>
    anchor_x: 'right'
    anchor_y: 'center'

<MatrixWidget>
    cols: 12
    rows: 12
    size_hint: .55, .7

<RootWidget>
    canvas.before:
        Color:
            rgba: .25, .25, .25, 1
        Rectangle:
            pos: self.pos
            size: self.size

    MatrixWidget:
        id:matrix
        spacing: 7
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        #canvas.before:
        #    Color:
        #        rgba: 0, 0, 0, 1
        #    Rectangle:
        #        pos: self.pos
        #        size: self.size

    MatrixTools:
        id:matrix_tools
        height: self.parent.height / 2
        size: 400, 400
        size_hint_x: .175
        size_hint_y: 0.375
        pos_hint: {'right': .975, 'center_y': .5}

    FloatLayout:
        id:prime_row
        TextInput:
            id:0
            size_hint: 0.038, 0.05
            pos_hint: {'center_x': 0.28, 'top': .93}
            font_size: self.height - 15
            multiline: False
            write_tab: False
        TextInput:
            id:1
            size_hint: 0.038, 0.05
            pos_hint: {'center_x': 0.32, 'top': .93}
            font_size: self.height - 15
            multiline: False
            write_tab: False
        TextInput:
            id:2
            size_hint: 0.038, 0.05
            pos_hint: {'center_x': 0.36, 'top': .93}
            font_size: self.height - 15
            multiline: False
            write_tab: False
        TextInput:
            id:3
            size_hint: 0.038, 0.05
            pos_hint: {'center_x': 0.4, 'top': .93}
            font_size: self.height - 15
            multiline: False
            write_tab: False
        TextInput:
            id:4
            size_hint: 0.038, 0.05
            pos_hint: {'center_x': 0.44, 'top': .93}
            font_size: self.height - 15
            multiline: False
            write_tab: False
        TextInput:
            id:5
            size_hint: 0.038, 0.05
            pos_hint: {'center_x': 0.48, 'top': .93}
            font_size: self.height - 15
            multiline: False
            write_tab: False
        TextInput:
            id:6
            size_hint: 0.038, 0.05
            pos_hint: {'center_x': 0.52, 'top': .93}
            font_size: self.height - 15
            multiline: False
            write_tab: False
        TextInput:
            id:7
            size_hint: 0.038, 0.05
            pos_hint: {'center_x': 0.56, 'top': .93}
            font_size: self.height - 15
            multiline: False
            write_tab: False
        TextInput:
            id:8
            size_hint: 0.038, 0.05
            pos_hint: {'center_x': 0.6, 'top': .93}
            font_size: self.height - 15
            multiline: False
            write_tab: False
        TextInput:
            id:9
            size_hint: 0.038, 0.05
            pos_hint: {'center_x': 0.64, 'top': .93}
            font_size: self.height - 15
            multiline: False
            write_tab: False
        TextInput:
            id:10
            size_hint: 0.038, 0.05
            pos_hint: {'center_x': 0.68, 'top': .93}
            font_size: self.height - 15
            multiline: False
            write_tab: False
        TextInput:
            id:11
            size_hint: 0.038, 0.05
            pos_hint: {'center_x': 0.72, 'top': .93}
            font_size: self.height - 15
            multiline: False
            write_tab: False

    ToolBarWidget:
        id: tools
        width: self.parent.width
        size_hint_y: 0.05
        pos_hint: {'center_x': 0.5, 'top': 1}
''')

class ToolBarWidget(AnchorLayout):
    '''
    This widget organizes it's children in a row, an of equal size.
    Contains three buttons by default. 
    '''
    def __init__(self, **kwargs):
        '''
        This method initializes the functions of 
        each button on the toolbar.
        By writing their functions in python 
        it allows for more precise control
        over the actions of each button. 
        '''
        super(ToolBarWidget, self).__init__(**kwargs)

        #The settings for each button to be added
        file_butt = Button(text="File")
        option_butt = Button(text="Options")
        exit_butt = Button(text="Exit", on_press=self.cls_func)

        self.add_widget(exit_butt)
        self.add_widget(option_butt)
        self.add_widget(file_butt)

    def cls_func(self, obj):
        '''
        This method safely closes the running application window.
        '''
        App.get_running_app().stop()
        Window.close()

    def do_layout(self, *args):
        '''
        This method is used to adjust the size of the toolbar
        for any incoming or outgoing widgets.
        The method ensures the toolbar fills the top of the app
        and that each widget has equal sizing.
        '''
        #Sets the variables needed for operation
        number_of_children = len(self.children)
        width = self.width
        width_per_child = width / number_of_children

        #posits determines the horizontal placement such that 
        #each widget comes directly after the other in a row.
        posits = range(0, int(width), int(width_per_child))
        for posit, child in zip(posits, self.children):
            child.height = self.height
            child.width = width_per_child
            child.x = self.x + posit
            child.y = self.y

    def on_size(self, *args):
        '''
        Adjusts sizes of widgets on resizing the window
        '''
        self.do_layout()

    def on_pos(self, *args):
        '''
        Adjusts sizes of widgets on repositioning any widget
        '''
        self.do_layout()

    def add_widget(self, widget):
        '''
        Adjusts sizes of widgets when adding a new widget
        '''
        super(ToolBarWidget, self).add_widget(widget)
        self.do_layout()

    def remove_widget(self, widget):
        '''
        Adjusts sizes of widgets when removing an old widget
        '''
        super(ToolBarWidget, self).remove_widget(widget)
        self.do_layout()

class MatrixTools(AnchorLayout):
    '''
    This widget arranges it's children in a column and of equal size. 
    By default it holds three buttons and two toolbarwidgets.
    '''
    def __init__(self, **kwargs):
        '''
        This method initializes the functions of 
        each button in the widget.
        By writing their functions in python 
        it allows for more precise control
        over the actions of each button. 
        '''
        super(MatrixTools, self).__init__(**kwargs)

        #Creates two new Toolbars and adds new buttons for each
        mini_tb1 = ToolBarWidget()
        mini_tb1.add_widget(Button(text="Flats", font_size=self.height - 85))
        mini_tb1.add_widget(Button(text="Sharps", font_size=self.height - 85))

        mini_tb2 = ToolBarWidget()
        mini_tb2.add_widget(Button(text="Expand", font_size=self.height - 85))
        mini_tb2.add_widget(Button(text="Alpha", font_size=self.height - 85))

        #Builds additional buttons to be added to the widget
        build_butt = Button(text="Build", font_size=self.height - 80)
        clear_butt = Button(text="Clear", font_size=self.height - 80)
        default_butt = Button(text="Default", font_size=self.height - 80)

        #Removes the original buttons from the toolbarwidgets
        for child in mini_tb1.children:
            if child.text != "Sharps" and child.text != "Flats":
                mini_tb1.remove_widget(child)
        mini_tb1.remove_widget(mini_tb1.children[2])

        for child in mini_tb2.children:
            if child.text != "Expand" and child.text != "Alpha":
                mini_tb2.remove_widget(child)
        mini_tb2.remove_widget(mini_tb2.children[2])

        self.add_widget(build_butt)
        self.add_widget(clear_butt)
        self.add_widget(mini_tb1)
        self.add_widget(mini_tb2)
        self.add_widget(default_butt)

    def do_layout(self, *args):
        '''
        This method is used to adjust the size of the widgets
        for any incoming or outgoing children.
        The method ensures the widget fills the space allocated
        and that each child has equal sizing.
        '''
        number_of_children = len(self.children)
        height = self.height
        height_per_child = height / number_of_children

        posits = range(0, int(height), int(height_per_child))
        for posit, child in zip(posits, self.children):
            child.width = self.width
            child.height = height_per_child
            child.x = self.x
            child.y = self.y + posit

    def on_size(self, *args):
        '''
        Adjusts sizes of widgets on resizing the window
        '''
        self.do_layout()

    def on_pos(self, *args):
        '''
        Adjusts sizes of widgets on repositioning any widget
        '''
        self.do_layout()

    def add_widget(self, widget):
        '''
        Adjusts sizes of widgets when adding a new widget
        '''
        super(MatrixTools, self).add_widget(widget)
        self.do_layout()

    def remove_widget(self, widget):
        '''
        Adjusts sizes of widgets when removing an old widget
        '''
        super(MatrixTools, self).remove_widget(widget)
        self.do_layout()

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