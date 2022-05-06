import sys

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.add(Gtk.Label(label=data))

class EditFbCellRenderer(Gtk.Box):
	def __init__(self, fb):
		super().__init__(*args, **kwargs)
		self.liststore = Gtk.ListStore(str, str)
		treeview =Gtk.TreeView(model=self.liststore)
		
		renderer_text = Gtk.CellRendererText()
		column_text = Gtk.TreeViewColumn("Type", renderer_text, text=0)
		treeview.append_column(column_text)
		
		renderer_editabletext = Gtk.CellRendererText()
		renderer_editabletext.set_property("editable", True)
		
		column_editabletext = Gtk.TreeViewColumn("", renderer_editabletext, text=1)
		treeview.append_column(column_editabletext)
		
		renderer_editabletext.connect("edited", self.text_edited)
		
		self.add(treeview)
	def text_edited(self, widget, path, text):
		self.liststore[path][1] = text	
	
class FBE_ListBox(Gtk.Box):
    def __init__(self, fb_editor):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=1)

        self.fb_editor = fb_editor

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
        self.cn_fb_button = self.add_toggle_button("Connect Events", self.connect_events, vbox_1)


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

        self.edit_fb_listbox = Gtk.ListBox()
        row = Gtk.ListBoxRow()
        hbox_2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        label = Gtk.Label(label="EVENTS:", xalign=0)
        row.add(hbox_2)
        hbox_2.pack_start(label, True, True, 0)
        label = Gtk.Label(label="	IN_EVENTS:", xalign=0)
        hbox_2.pack_start(label, True, True, 0)

        self.edit_fb_listbox.add(row)
        self.pack_start(self.edit_fb_listbox, True, True , 0)

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

    def on_type_changed(self, combo):
        selected = combo.get_active_text()
        event_driven = ["PERMIT", "E_CTU", "E_MERGE","E_RESTART", "E_CYCLE", "E_DELAY", "E_DEMUX"]
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

    def create_edit_fb_listbox(self, listbox, fb):
        pass


