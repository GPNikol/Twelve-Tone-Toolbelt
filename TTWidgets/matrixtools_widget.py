'''
CREATED BY: Gregory P. Nikol
MOST RECENT UPDATE: December 14, 2018

Class for building, clearing, and modifying the appearence of the matrix widget
'''
import kivy
kivy.require('1.10.1')

from .toolbar_widget import ToolBarWidget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button

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

