#! /usr/bin/python3

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class ExecuteWindow(Gtk.Box):
    def __init__(self, diagram, *args, **kwargs):
        super().__init__(orientation = Gtk.Orientation.VERTICAL, *args, **kwargs)

        self.listbox = Gtk.ListBox()
        self.diagram = diagram
        print(diagram)
        
        init_button = Gtk.Button().new_with_label("Execute")
        init_button.connect("clicked", self.on_execute)
        init_fb_entry = Gtk.Entry()
        init_fb_entry.set_width_chars(7)
        init_fb_entry.set_text("Starting Function Block")
        init_fb_entry.connect("changed", self.on_init_fb_changed)
        self.spinbutton = Gtk.SpinButton()
        adjustment = Gtk.Adjustment(upper=100, step_increment=0.5, page_increment=10)
        self.spinbutton.set_adjustment(adjustment)
        self.spinbutton.set_digits(1)
        self.spinbutton.connect("value-changed", self.on_value_changed)
        

        self.exec_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.exec_box.pack_start(init_button, False, False, 0)
        self.exec_box.pack_start(self.spinbutton, False, False, 0)

        self.listbox.add(init_fb_entry)
        self.listbox.add(self.exec_box)
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)	
        self.pack_start(self.listbox, True, True, 0)
        self.listbox.show_all()
        


    def on_execute(self, button):
        pass
    
    def on_init_fb_changed(self, widget):
        pass
	
    def on_value_changed(self, button):
        pass
