#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio
import sys
from gui.fb_editor import Function_Block_Editor
from gui.fbe_listbox import FBE_ListBox
from types_and_conversions.py_xml import *

class Window(Gtk.ApplicationWindow):
    def __init__(self, app):
        super(Window, self).__init__(title="GASR-FBE2", application=app)

        self.main_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        self.box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.main_box.pack_start(self.box, True, True, 0)

        self.menubar = Gtk.MenuBar()
        self.function_block_editor = Function_Block_Editor()
        fmi = self.create_sub_menu("File")
        self.create_simple_menu_item(fmi, New=self.quitApp, Save=self.quitApp, Save_As=None, Import_FB=self.load_function_block)

        nmi = self.create_sub_menu('Not File')
        self.create_simple_menu_item(nmi, DONT_SAVE = self.quitApp)

        listbox = FBE_ListBox(self.function_block_editor)

        self.box.pack_start(self.menubar, False, True, 0)
        self.box.pack_start(self.function_block_editor, True, True, 0)	
        self.main_box.pack_start(listbox, False, False, 0)

        self.add(self.main_box)

        self.set_default_size(800, 600)

    def quitApp(self, par):

        app.quit()    
	
    def load_function_block(self, par):
		
        setattr(self.function_block_editor.function_block_renderer.fb_diagram, "E_SPLIT", convert_xml_basic_fb("types_and_conversions/E_SPLIT.fbt"))
        self.function_block_editor.function_block_renderer.fb_diagram.add_function_block(convert_xml_basic_fb("types_and_conversions/E_SPLIT.fbt"))
	
    def create_sub_menu(self, label):
        sub_menu = Gtk.MenuItem.new_with_label(label)
        self.menubar.add(sub_menu)
        return sub_menu

    def create_simple_menu_item(self, sub_menu, **kwargs): # kwargs are so-> label: function
        menu = Gtk.Menu()

        for label in kwargs.keys():
            menu_item = Gtk.MenuItem.new_with_label(label)
            try:
                menu_item.connect("activate", kwargs[label])
                menu.append(menu_item)
            except:
                menu.append(menu_item)
        sub_menu.set_submenu(menu)




class Application(Gtk.Application):

    def __init__(self):
        super(Application, self).__init__()

    def do_activate(self):

        self.win = Window(self)
        self.win.show_all()

    def do_startup(self):

        Gtk.Application.do_startup(self)

app = Application()
app.run(sys.argv)
