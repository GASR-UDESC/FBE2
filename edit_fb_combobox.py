#!/usr/bin/python3
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class CellRendererTextWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="CellRendererText Example")

        self.set_default_size(200, 200)

        self.liststore = Gtk.ListStore(str, str)
        self.liststore.append(["IN EVENTS", "EI: True | INIT: True"])
        self.liststore.append(["OUT EVENTS", "EO: False | INITO: True"])
        self.liststore.append(["IN VARIABLES", "PERMIT: True"])
        self.liststore.append(["OUT VARIABLES", ""])

        treeview = Gtk.TreeView(model=self.liststore)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Type", renderer_text, text=0)
        treeview.append_column(column_text)

        renderer_editabletext = Gtk.CellRendererText()
        renderer_editabletext.set_property("editable", True)

        column_editabletext = Gtk.TreeViewColumn(
            "", renderer_editabletext, text=1
        )
        treeview.append_column(column_editabletext)

        renderer_editabletext.connect("edited", self.text_edited)

        self.add(treeview)

    def text_edited(self, widget, path, text):
        self.liststore[path][1] = text


win = CellRendererTextWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
