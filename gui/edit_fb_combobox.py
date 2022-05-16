#! /usr/bin/python3

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class EditFunctionBlockWindow(Gtk.Box):
    def __init__(self, fb, *args, **kwargs):
        super().__init__(orientation = Gtk.Orientation.VERTICAL, *args, **kwargs)


        self.listbox = Gtk.ListBox()
        self.refresh(fb)
        # ~ self.new_event_name = None		
		
        self.pack_start(self.listbox, True, True, 0)
        self.listbox.show_all()

    def text_edited(self, widget, path, text):
        self.liststore[path][1] = text

    def refresh(self, fb):
        self.listbox.unselect_all()
        out_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        in_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        for item in self.listbox.get_children():
            self.listbox.remove(item)
        
        row_in = Gtk.ListBoxRow()
        row_out = Gtk.ListBoxRow()
        hbox_in = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        hbox_out = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        
        if fb != None:  
            label_in = Gtk.Label("In Events    ", xalign=0)
            label_out = Gtk.Label("Out Events   ", xalign=0)
            for event in fb.events.items():
				
                if event[1].active == None:
                    active = "None"
                else:
                    active = str(event[1].active)
                if event[1].in_event:
                    label = Gtk.Label(event[0] + ": " + active, xalign=0)
                    in_box.pack_start(label, True, True, 0)
                else:
                    label = Gtk.Label(event[0] + ": " + active, xalign=0)
                    out_box.pack_start(label, True, True, 0)
            try:
                hbox_in.pack_start(label_in, True, True, 0) 
                hbox_in.pack_start(in_box, True, True, 0) 

                hbox_out.pack_start(label_out, True, True, 0)
                hbox_out.pack_start(out_box, True, True, 0)
            except:
                pass
            row_in.add(hbox_in)
            row_out.add(hbox_out)
            self.listbox.add(row_in)
            self.listbox.add(row_out)
            self.listbox.show_all()
			
            label_in = Gtk.Label("In Variables ", xalign=0)
            label_out = Gtk.Label("Out Variables", xalign=0)
            out_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            in_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            row_in = Gtk.ListBoxRow()
            row_out = Gtk.ListBoxRow()
            hbox_in = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
            hbox_out = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
			
            for variable in fb.variables.items():
				
                if variable[1].value == None:
                    active = "None"
                else:
                    active = str(variable[1].value)
                if variable[1].in_var:
                    label = Gtk.Label(variable[0] + ": " + active, xalign=0)
                    in_box.pack_start(label, True, True, 0)
                else:
                    label = Gtk.Label(variable[0] + ": " + active, xalign=0)
                    out_box.pack_start(label, True, True, 0)
            try:
                hbox_in.pack_start(label_in, True, True, 0) 
                hbox_in.pack_start(in_box, True, True, 0) 

                hbox_out.pack_start(label_out, True, True, 0)
                hbox_out.pack_start(out_box, True, True, 0)
            except:
                pass
            row_in.add(hbox_in)
            row_out.add(hbox_out)
            self.listbox.add(row_in)
            self.listbox.add(row_out)
            self.listbox.show_all()
			




