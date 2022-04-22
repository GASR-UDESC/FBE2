import sys

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.add(Gtk.Label(label=data))


class FBE_ListBox(Gtk.Box):
    def __init__(self, fb_editor):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=1)

        self.fb_editor = fb_editor

        event_driven = ["PERMIT", "E_CTU", "E_MERGE"]
        service_interface = ["IO_WRITER", "IO_READER", "PID_SIMPLE"]


        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.pack_start(listbox, True, True, 0)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        row.add(hbox)
        vbox_1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(vbox_1, True, True, 0)

        self.add_toggle_button("Add Function Block", self.add_function_block, vbox_1)
        # ~ self.add_button("Remove Function Block", self.rem_function_block, vbox_1)

        listbox.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        row.add(hbox)
        label = Gtk.Label(label="Enable/Disable", xalign=0)
        check = Gtk.CheckButton()
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(check, False, True, 0)

        listbox.add(row)
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        row.add(hbox)
        label = Gtk.Label(label="Function Block Type", xalign=0)
        combo = Gtk.ComboBoxText()
        self.add_combo_box_item(combo, 0, 'event-driven', "Event Driven")
        self.add_combo_box_item(combo, 1, 'service-interface', "Service Interface")
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(combo, False, True, 0)

        listbox.add(row)

        self.add_fb_listbox = Gtk.ListBox()
        combo.connect("changed", self.on_type_changed)

        self.add_fb_listbox.connect("row-activated", self.on_row_activated)


    def add_button(self, label, function, box):
        button = Gtk.Button.new_with_label(label)
        button.connect("clicked", function)
        box.pack_start(button, False, False, 0)

    def add_toggle_button(self, label, function, box):
        button = Gtk.ToggleButton.new_with_label(label)
        button.connect("toggled", self.add_function_block)
        box.pack_start(button, False, False, 0)

    def add_combo_box_item(self, combo, pos, _id, label):
        combo.insert(pos, _id, label)

    def add_function_block(self, button):

        if self.add_fb_listbox in self.get_children():
            self.remove(self.add_fb_listbox)
            self.fb_editor.enable_add = False
        else:
            self.pack_start(self.add_fb_listbox, True, True, 0)
            self.fb_editor.enable_add = True

    def rem_function_block(self, button):
        print(button)

    def on_row_activated(self, listbox_widget, row):
        print(row.data)
        self.fb_editor.selected_fb = row.data

    def on_type_changed(self, combo):
        selected = combo.get_active_text()
        event_driven = ["PERMIT", "E_CTU", "E_MERGE"]
        service_interface = ["IO_WRITER", "IO_READER", "PID_SIMPLE"]
        selected_type = list()
        if selected == 'Event Driven':
            selected_type = event_driven
        elif selected == 'Service Interface':
            selected_type = service_interface
        for item in self.add_fb_listbox.get_children():
            self.add_fb_listbox.remove(item)

        for item in selected_type:
            self.add_fb_listbox.add(ListBoxRowWithData(item))
        self.add_fb_listbox.show_all()
