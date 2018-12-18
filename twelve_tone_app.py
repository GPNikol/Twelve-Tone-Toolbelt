'''
CREATED BY: Gregory P. Nikol
MOST RECENT UPDATE: December 14, 2018

This script provides a GUI interface for a Twelve Tone Matrix.

It has been adapted from a previous - terminal based application
to work as a Python Kivy Application.
'''
import kivy
import kivy.uix.settings
kivy.require('1.10.1')

from TTWidgets import RootWidget

from kivy.app import App
from kivy.logger import Logger

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