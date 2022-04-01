#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio
import sys


class Window(Gtk.ApplicationWindow):

    def __init__(self, app):
        super(Window, self).__init__(title="GASR-FBE2", application=app)

        self.grid = Gtk.Grid()

        menubar = Gtk.MenuBar()

        fmi = Gtk.MenuItem.new_with_label("File")

        menu = Gtk.Menu()
        emi = Gtk.MenuItem.new_with_label("New") 
        emi.connect("activate", self.quitApp)
        menu.append(emi)

        emi = Gtk.MenuItem.new_with_label("Save") 
        emi.connect("activate", self.init_drawing_area)
        menu.append(emi)

        emi = Gtk.MenuItem.new_with_label("Save as") 
        emi.connect("activate", self.quitApp)
        menu.append(emi)


        emi = Gtk.MenuItem.new_with_label("Save as") 
        emi.connect("activate", self.quitApp)
        menu.append(emi)

        fmi.set_submenu(menu)

        menubar.add(fmi)

        self.grid.attach(menubar, 0, 1, 1, 1)

        self.add(self.grid)

        self.set_default_size(400, 600)

    def quitApp(self, par):

        app.quit()    

    def init_drawing_area(self, par):
        darea = Gtk.DrawingArea()
        darea.connect("draw", self.on_draw)
        self.grid.attach(darea, 0, 0, 1, 1)

        self.set_title("Basic Shapes")
        self.set_default_size(400, 400)

        self.connect("destroy", Gtk.main_quit)

    def on_draw(self, da, ctx):

        ctx.set_source_rgb(0.6, 0.6, 0.6)

        ctx.rectangle(20, 20, 120, 80)
        ctx.rectangle(180, 20, 80, 80)
        ctx.fill()


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
