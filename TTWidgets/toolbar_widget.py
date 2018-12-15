'''
CREATED BY: Gregory P. Nikol
MOST RECENT UPDATE: December 14, 2018

Class for altering the function  or appearence of the twelve tone app
'''
import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button

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
