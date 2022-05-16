#! /usr/bin/python3

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class EditFunctionBlockWindow(Gtk.Box):
    def __init__(self, fb, *args, **kwargs):
        super().__init__(orientation = Gtk.Orientation.VERTICAL, *args, **kwargs)


        self.liststore = Gtk.ListStore(str, str)
        self.refresh(fb)
        # ~ self.new_event_name = None
        treeview = Gtk.TreeView(model=self.liststore)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Type", renderer_text, text=0)
        treeview.append_column(column_text)

        renderer_editabletext = Gtk.CellRendererText()
        renderer_editabletext.set_property("editable", False)

        column_editabletext = Gtk.TreeViewColumn(
                "", renderer_editabletext, text=1
                )
        treeview.append_column(column_editabletext)

        renderer_editabletext.connect("edited", self.text_edited)

        self.pack_start(treeview, True, True, 0)

    def text_edited(self, widget, path, text):
        self.liststore[path][1] = text

    def refresh(self, fb):
        in_evt_str = ""
        out_evt_str = ""
        in_var_str = ""
        out_var_str = ""
        name = ""
        self.liststore.clear()

        if fb != None:
            for event in fb.events.items():
                if event[1].active == None:
                    active = "None"
                else:
                    active = str(event[1].active)
                if event[1].in_event:
                    in_evt_str = in_evt_str + "(" + event[0] + ": " + active + ") "
                else:
                    out_evt_str = out_evt_str + "(" + event[0] + ": " + active + ") "

            for var in fb.variables.items():
                if var[1].value == None:
                    value = "None"
                else:
                    value = str(var[1].value)
                if var[1].in_var:
                    in_var_str =  in_var_str + "(" + var[0] + ": " + value + ") "
                else:
                    out_var_str = out_var_str + "(" + var[0] + ": " + value + ") "
            name = fb.name

        self.liststore.append(["Name:", name])
        self.liststore.append(["In Events:", in_evt_str])
        self.liststore.append(["Out Events:", out_evt_str])
        self.liststore.append(["In Variables:", in_var_str])
        self.liststore.append(["Out Variables:", out_var_str])


