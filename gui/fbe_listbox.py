import sys

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from function_block.function_block import Event
from function_block.function_block import Variable
from function_block.function_block import world

class AddDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Add", flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        self.if_in = Gtk.CheckButton()
        if_in_label = Gtk.Label("In")
        self.set_default_size(150, 70)

        self.entry = Gtk.Entry.new()
        # ~ self.entry_value = self.entry.get_text()

        box = self.get_content_area()
        box.add(self.entry)
        
        check_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        check_box.pack_start(if_in_label, True, True, 0)
        check_box.pack_start(self.if_in, True, True, 0)
        
        box.add(check_box)
        
        
        self.show_all()
		
		
class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.add(Gtk.Label(label=data))

class FBE_ListBox(Gtk.Box):
    def __init__(self, fb_editor):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=1)

        self.fb_editor = fb_editor
        self.fb_import_list = set()
		
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.pack_start(listbox, True, True, 0)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        row.add(hbox)
        vbox_1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(vbox_1, True, True, 0)

        self.add_fb_button = self.add_toggle_button("Add Function Block", self.add_function_block, vbox_1)
        self.rm_fb_button = self.add_toggle_button("Delete", self.delete, vbox_1)
        self.cn_fb_button = self.add_toggle_button("Connect", self.connect_events, vbox_1)


        listbox.add(row)

        # ~ row = Gtk.ListBoxRow()
        # ~ hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        # ~ row.add(hbox)
        # ~ label = Gtk.Label(label="Enable/Disable", xalign=0)
        # ~ check = Gtk.CheckButton()
        # ~ hbox.pack_start(label, True, True, 0)
        # ~ hbox.pack_start(check, False, True, 0)

        # ~ listbox.add(row)
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        row.add(hbox)
        label = Gtk.Label(label="Function Block Type", xalign=0)
        # ~ combo = Gtk.ComboBoxText()
        # ~ self.add_combo_box_item(combo, 0, 'event-driven', "Event Driven")
        # ~ self.add_combo_box_item(combo, 1, 'service-interface', "Service Interface")
        hbox.pack_start(label, True, True, 0)
        # ~ hbox.pack_start(combo, False, True, 0)

        listbox.add(row) # belongs to Fucntion Block Type

        self.add_fb_listbox = Gtk.ListBox()
        # ~ combo.connect("changed", self.on_type_changed)

        self.add_fb_listbox.connect("row-activated", self.on_row_activated)

        for item in self.fb_import_list:
            self.add_fb_listbox.add(ListBoxRowWithData(item))
        self.add_fb_listbox.show_all()
        
        self.edit_fb_listbox = Gtk.ListBox()
        row = Gtk.ListBoxRow()
        row.add(self.fb_editor.edit_fb_window)

        self.edit_fb_listbox.add(row)
        self.pack_start(self.edit_fb_listbox, True, True , 0)
        self.add_button("Add Event", self.add_event, self.fb_editor.edit_fb_window)
        self.add_button("Add Variable", self.add_variable, self.fb_editor.edit_fb_window)
        self.add_button("Change Name", self.change_name, self.fb_editor.edit_fb_window)
        self.add_button("Execute", self.on_execute, self.fb_editor.edit_fb_window)
		
    def add_button(self, label, function, box):
        button = Gtk.Button.new_with_label(label)
        button.connect("clicked", function)
        box.pack_start(button, False, False, 0)


    def add_toggle_button(self, label, function, box):
        button = Gtk.ToggleButton.new_with_label(label)
        button.connect("toggled", function)
        box.pack_start(button, False, False, 0)
        return button

    def add_combo_box_item(self, combo, pos, _id, label):
        combo.insert(pos, _id, label)

    def add_function_block(self, button):
        
        self.add_fb_listbox.unselect_all()
        if self.add_fb_listbox in self.get_children():
            self.remove(self.add_fb_listbox)
            self.fb_editor.enable_add = False
            self.pack_start(self.edit_fb_listbox, True, True, 0)
        else:
            self.remove(self.edit_fb_listbox)
            self.rm_fb_button.set_active(False)
            self.cn_fb_button.set_active(False)
            self.pack_start(self.add_fb_listbox, True, True, 0)
            self.fb_editor.enable_add = True
            for item in self.add_fb_listbox.get_children():
                self.add_fb_listbox.remove(item)
            for item in self.fb_import_list:
                self.add_fb_listbox.add(ListBoxRowWithData(item))
            self.add_fb_listbox.show_all()
	
    def add_event(self, button):
        dialog = AddDialog(self)
        response = dialog.run()
        entry = dialog.entry.get_text()

        if response == Gtk.ResponseType.OK:
            print(entry)
            self.fb_editor.selected_fb.add_event(entry, Event(self.fb_editor.selected_fb, False, in_event = dialog.if_in.get_active()))		
        elif response == Gtk.ResponseType.CANCEL:
            pass

        dialog.destroy()
        
    def add_variable(self, button):
        dialog = AddDialog(self)
        response = dialog.run()
        entry = dialog.entry.get_text()

        if response == Gtk.ResponseType.OK:
            print(entry)
            self.fb_editor.selected_fb.add_variable(entry, Variable(self.fb_editor.selected_fb, False, in_var = dialog.if_in.get_active()))		
        elif response == Gtk.ResponseType.CANCEL:
            pass

        dialog.destroy()

    def change_name(self, button):
        dialog = AddDialog(self)
        response = dialog.run()
        entry = dialog.entry.get_text()

        if response == Gtk.ResponseType.OK:
            print(entry)
            self.fb_editor.selected_fb.name = entry		
        elif response == Gtk.ResponseType.CANCEL:
            pass

        dialog.destroy()

    def delete(self, button):
        if self.fb_editor.enable_remove:
            self.fb_editor.enable_remove = False
        else:
            self.fb_editor.enable_remove = True
            self.add_fb_button.set_active(False)
            self.cn_fb_button.set_active(False)

    def connect_events(self, button):
        if self.fb_editor.enable_connect:
            self.fb_editor.enable_connect = False
        else:
            self.fb_editor.enable_connect = True
            self.add_fb_button.set_active(False)
            self.rm_fb_button.set_active(False)

    def on_row_activated(self, listbox_widget, row):
        print(row.data)
        self.fb_editor.selected_fb = row.data

    def on_execute(self, button):
		self.fb_editor.function_block_renderer.fb_diagram.E_RESTART.WARM.active = True
        self.fb_editor.function_block_renderer.fb_diagram.execute(i_fb=self.fb_editor.function_block_renderer.fb_diagram.E_RESTART, draw_fn=self.fb_editor.function_block_renderer.queue_draw)
		
    # ~ def on_type_changed(self, combo):
        # ~ selected = combo.get_active_text()
        # ~ event_driven = ["PERMIT", "E_CTU", "E_MERGE","E_RESTART", "E_CYCLE", "E_DELAY", "E_DEMUX"]
        # ~ service_interface = ["IO_WRITER", "IO_READER", "PID_SIMPLE", "Base Function Block"]
        # ~ selected_type = list()
        # ~ if selected == 'Event Driven':
            # ~ selected_type = event_driven
        # ~ elif selected == 'Service Interface':
            # ~ selected_type = service_interface
        # ~ print(self.fb_import_list)
        # ~ for item in self.add_fb_listbox.get_children():
            # ~ self.add_fb_listbox.remove(item)

        # ~ for item in self.fb_import_list:
            # ~ self.add_fb_listbox.add(ListBoxRowWithData(item))
        # ~ self.add_fb_listbox.show_all()

    def create_edit_fb_listbox(self, listbox, fb):
        pass


