#! /usr/bin/python3

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class EditFunctionBlockWindow(Gtk.Box):
    def __init__(self, fb, *args, **kwargs):
        super().__init__(orientation = Gtk.Orientation.VERTICAL, *args, **kwargs)


        self.listbox = Gtk.ListBox()
        self.fb = fb
        self.in_event_text = Gtk.Entry()
        self.out_event_text = Gtk.Entry()
        self.in_var_text = Gtk.Entry()
        self.out_var_text = Gtk.Entry()
        self.selected_in_event = None
        self.selected_out_event = None
        self.selected_in_var = None
        self.selected_out_var = None
        
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.refresh(fb)
        # ~ self.new_event_name = None		
		
        self.pack_start(self.listbox, True, True, 0)
        self.listbox.show_all()


    def refresh(self, fb):
        self.in_event_text = Gtk.Entry()
        self.out_event_text = Gtk.Entry()
        # ~ self.out_event_text.set_editable(False)
        self.in_var_text = Gtk.Entry()
        self.out_var_text = Gtk.Entry()
        
        self.in_event_text.set_width_chars(5)
        self.out_event_text.set_width_chars(5)
        self.in_var_text.set_width_chars(5)
        self.out_var_text.set_width_chars(5)
        
        self.in_event_text.connect("changed", self.on_in_event_text_changed)
        self.out_event_text.connect("changed", self.on_out_event_text_changed)
        self.in_var_text.connect("changed", self.on_in_var_text_changed)
        self.out_var_text.connect("changed", self.on_out_var_text_changed)
        self.fb = fb
        self.listbox.unselect_all()
        # ~ out_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        # ~ in_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        for item in self.listbox.get_children():
            self.listbox.remove(item)
        
        row_in = Gtk.ListBoxRow()
        row_out = Gtk.ListBoxRow()
        hbox_in = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        hbox_out = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        
        if fb != None:  
            label_in = Gtk.Label("In Events    ", xalign=0)
            label_out = Gtk.Label("Out Events   ", xalign=0)
            
            in_store = Gtk.ListStore(str)
            out_store = Gtk.ListStore(str)
			
			
            for event in fb.events.items():
				
                if event[1].active == None:
                    active = "None"
                else:
                    active = str(event[1].active)
                if event[1].in_event:
                    # ~ print(event[0], active)
                    in_store.append([event[0]])
                else:
                    out_store.append([event[0]])
			
            in_event_combobox = Gtk.ComboBox.new_with_model(in_store)
            in_event_combobox.connect("changed", self.on_event_changed)
            in_renderer_text = Gtk.CellRendererText()
            in_event_combobox.pack_start(in_renderer_text, True)
            in_event_combobox.add_attribute(in_renderer_text, "text", 0)
            
            out_event_combobox = Gtk.ComboBox.new_with_model(out_store)
            out_event_combobox.connect("changed", self.on_event_changed)
            out_renderer_text = Gtk.CellRendererText()
            out_event_combobox.pack_start(out_renderer_text, True)
            out_event_combobox.add_attribute(out_renderer_text, "text", 0)
			
            try:
                hbox_in.pack_start(label_in, True, True, 0) 
                hbox_in.pack_start(in_event_combobox, False, False, 0) 
                hbox_in.pack_start(self.in_event_text, False, False, 0)

                hbox_out.pack_start(label_out, True, True, 0)
                hbox_out.pack_start(out_event_combobox, False, False, 0)
                hbox_out.pack_start(self.out_event_text, False, False, 0)
            except:
                pass
                
            row_in.add(hbox_in)
            row_out.add(hbox_out)
            self.listbox.add(row_in)
            self.listbox.add(row_out)
            self.listbox.show_all()
			
            row_in = Gtk.ListBoxRow()
            row_out = Gtk.ListBoxRow()
            hbox_in = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
            hbox_out = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
            

            label_in = Gtk.Label("In Variables    ", xalign=0)
            label_out = Gtk.Label("Out Variables   ", xalign=0)
            
            in_store = Gtk.ListStore(str)
            out_store = Gtk.ListStore(str)
                                    
                                    
            for var in fb.variables.items():
                                                    
                if var[1].value == None:
                        active = "None"
                else:
                        active = str(event[1].active)
                if var[1].in_var:
                        # ~ print(event[0], active)
                        in_store.append([var[0]])
                else:
                        out_store.append([var[0]])
                                    
            in_var_combobox = Gtk.ComboBox.new_with_model(in_store)
            in_var_combobox.connect("changed", self.on_var_changed)
            in_renderer_text = Gtk.CellRendererText()
            in_var_combobox.pack_start(in_renderer_text, True)
            in_var_combobox.add_attribute(in_renderer_text, "text", 0)
            
            out_var_combobox = Gtk.ComboBox.new_with_model(out_store)
            out_var_combobox.connect("changed", self.on_var_changed)
            out_renderer_text = Gtk.CellRendererText()
            out_var_combobox.pack_start(out_renderer_text, True)
            out_var_combobox.add_attribute(out_renderer_text, "text", 0)
                                    
            hbox_in.pack_start(label_in, True, True, 0) 
            hbox_in.pack_start(in_var_combobox, False, False, 0) 
            hbox_in.pack_start(self.in_var_text, False, False, 0)

            hbox_out.pack_start(label_out, True, True, 0)
            hbox_out.pack_start(out_var_combobox, False, False, 0)
            hbox_out.pack_start(self.out_var_text, False, False, 0)
                    
            row_in.add(hbox_in)
            row_out.add(hbox_out)
            self.listbox.add(row_in)
            self.listbox.add(row_out)
            self.listbox.show_all()

    def on_event_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            event = model[tree_iter][0]
            print("Selected: event =%s" % event)
            if self.fb.events[event].in_event:
                self.selected_in_event = event
				
            else:
                self.selected_out_event = event
				
            if self.fb.events[event].in_event:
                self.in_event_text.set_text(str(self.fb.events[event].active))
            else:
                self.out_event_text.set_text(str(self.fb.events[event].active))

    def on_var_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            var = model[tree_iter][0]
            print("Selected: event =%s" % var)
            if self.fb.variables[var].in_var:
                self.selected_in_var = var
				
            else:
                self.selected_out_var = var
				
            if self.fb.variables[var].in_var:
                if self.fb.variables[var].value != None:
                    self.in_var_text.set_text(str(self.fb.variables[var].value))
                else:
                    self.in_var_text.set_text("None")
            else:
                if self.fb.variables[var].value != None:
                    self.out_var_text.set_text(str(self.fb.variables[var].value))
                else:	
                    self.out_var_text.set_text("None")

    def on_in_event_text_changed(self, entry):
        if entry.get_text() == "False":
            getattr(self.fb, self.selected_in_event).active = False
        elif entry.get_text() == "True":
            getattr(self.fb, self.selected_in_event).active = True
			
    def on_out_event_text_changed(self, entry):
        if entry.get_text() == "False":
            getattr(self.fb, self.selected_out_event).active = False
        elif entry.get_text() == "True":
            getattr(self.fb, self.selected_out_event).active = True
			
    def on_in_var_text_changed(self, entry):
        try:
            _type = getattr(self.fb, self.selected_in_var).type
            if _type == "BOOL":
                getattr(self.fb, self.selected_in_var).value = bool(entry.get_text())
            elif _type == "UINT":
                getattr(self.fb, self.selected_in_var).value = int(entry.get_text())
            elif _type == "REAL":
                getattr(self.fb, self.selected_in_var).value = float(entry.get_text())
            elif _type == "BYTES":
                getattr(self.fb, self.selected_in_var).value = bytes(entry.get_text())
            elif _type == "STRING":
                getattr(self.fb, self.selected_in_var).value = str(entry.get_text())
            else:
                print("Unrecognized variable type")
        except:
            pass

    def on_out_var_text_changed(self, entry):
        try:
            _type = getattr(self.fb, self.selected_out_var).type
            if _type == "BOOL":
                getattr(self.fb, self.selected_out_var).value = bool(entry.get_text())
            elif _type == "UINT":
                getattr(self.fb, self.selected_out_var).value = int(entry.get_text())
            elif _type == "REAL":
                getattr(self.fb, self.selected_out_var).value = float(entry.get_text())
            elif _type == "BYTES":
                getattr(self.fb, self.selected_out_var).value = bytes(entry.get_text())
            elif _type == "STRING":
                getattr(self.fb, self.selected_out_var).value = str(entry.get_text())
            else:
                print("Unrecognized variable type")
        except:
            pass
