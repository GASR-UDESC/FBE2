#!/usr/bin/python
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio



class MainWindow(Gtk.ApplicationWindow):
    def __init__(self):
        Gtk.Window.__init__(self, title="EBF")
        self.set_default_size(400, 300)
        layout = Gtk.Box()
        
        layout2 = Gtk.Box()
        self.add(layout)
        self.add(layout2)

        main_menu_bar = Gtk.MenuBar()
        
        file_menu = Gtk.Menu()
        file_menu_dropdown = Gtk.MenuItem("File")
        
        file_new = Gtk.MenuItem("new")
        file_save = Gtk.MenuItem("save")
        file_save_as = Gtk.MenuItem("save as")
        file_close = Gtk.MenuItem("close")
        
        file_menu_dropdown.set_submenu(file_menu)
        file_menu.append(file_new)
        file_menu.append(file_save)
        file_menu.append(file_save_as)
        file_menu.append(Gtk.SeparatorMenuItem())
        file_menu.append(file_close)
        
        main_menu_bar.append(file_menu_dropdown)
        layout.pack_start(main_menu_bar, True, True, 0)
        
        

window = MainWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
















