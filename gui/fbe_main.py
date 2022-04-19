#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio
import sys
from fb_editor import Function_Block_Editor


class Window(Gtk.ApplicationWindow):

    def __init__(self, app):
        super(Window, self).__init__(title="GASR-FBE2", application=app)

        self.box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        self.menubar = Gtk.MenuBar()
        function_block_editor = Function_Block_Editor()
        fmi = self.create_sub_menu("File")
        self.create_simple_menu_item(fmi, New=self.quitApp, Save=self.quitApp, Save_As=self.quitApp)

        nmi = self.create_sub_menu('Not File')
        self.create_simple_menu_item(nmi, DONT_SAVE = self.quitApp)

        self.box.pack_start(self.menubar, False, True, 0)
        self.box.pack_start(function_block_editor, True, True, 0)	

        self.add(self.box)

        self.set_default_size(400, 600)

    def quitApp(self, par):

        app.quit()    

    def create_sub_menu(self, label):
        sub_menu = Gtk.MenuItem.new_with_label(label)
        self.menubar.add(sub_menu)
        return sub_menu

    def create_simple_menu_item(self, sub_menu, **kwargs): # kwargs are so-> label: function
        menu = Gtk.Menu()

        for label in kwargs.keys():
            menu_item = Gtk.MenuItem.new_with_label(label)
            menu_item.connect("activate", kwargs[label])
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
