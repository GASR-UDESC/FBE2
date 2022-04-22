#!/usr/bin/python

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.add(Gtk.Label(label=data))


class ListBoxWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="ListBox Demo")
        self.set_border_width(10)

        event_driven = ["PERMIT", "E_CTU", "E_MERGE"]
        service_interface = ["IO_WRITER", "IO_READER", "PID_SIMPLE"]

        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        self.add(box_outer)

        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        box_outer.pack_start(listbox, True, True, 0)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        row.add(hbox)
        vbox_1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(vbox_1, True, True, 0)

        self.add_button("Add Function Block", self.add_function_block, vbox_1)
        self.add_button("Remove Function Block", self.rem_function_block, vbox_1)

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

        self.listbox_2 = Gtk.ListBox()
        combo.connect("changed", self.on_type_changed)

        for item in event_driven:
            self.listbox_2.add(ListBoxRowWithData(item))

        def sort_func(row_1, row_2, data, notify_destroy):
            return row_1.data.lower() > row_2.data.lower()

        def filter_func(row, data, notify_destroy):
            return False if row.data == "Fail" else True

        self.listbox_2.set_sort_func(sort_func, None, False)
        self.listbox_2.set_filter_func(filter_func, None, False)

        def on_row_activated(listbox_widget, row):
            print(row.data)

        self.listbox_2.connect("row-activated", on_row_activated)

        box_outer.pack_start(self.listbox_2, True, True, 0)
        self.listbox_2.show_all()

    def add_button(self, label, function, box):
        button = Gtk.Button.new_with_label(label)
        button.connect("clicked", function)
        box.pack_start(button, False, False, 0)

    def add_combo_box_item(self, combo, pos, _id, label):
        combo.insert(pos, _id, label)

    def add_function_block(self, button):
        print(button)

    def rem_function_block(self, button):
        print(button)

    def on_type_changed(self, combo):
        selected = combo.get_active_text()
        event_driven = ["PERMIT", "E_CTU", "E_MERGE"]
        service_interface = ["IO_WRITER", "IO_READER", "PID_SIMPLE"]
        selected_type = list()
        if selected == 'Event Driven':
            selected_type = event_driven
        elif selected == 'Service Interface':
            selected_type = service_interface
        for item in self.listbox_2.get_children():
            self.listbox_2.remove(item)


        for item in selected_type:
            self.listbox_2.add(ListBoxRowWithData(item))
        self.listbox_2.show_all()



win = ListBoxWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
