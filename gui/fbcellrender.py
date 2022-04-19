#! /usr/bin/python3

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


software_list = [
        ("PERMIT", "Event Driven"),
        ("E_CTU", "Event Driven"),
        ("E_MERGE", "Event Driven"),
        ("E_DEMUX", "Event Driven"),
        ("E_DELAY", "Event Driven"),
        ("E_RESTART", "Event Driven"),
        ("E_CYCLE", "Event Driven"),
        ("E_DELAY", "Event Driven"),
        ("E_RESTART", "Event Driven"),
        ("IO_WRITER", "SIFB"),
        ("IO_READER", "SIFB"),
        ("PID_SIMPLE","SIFB"),
        ]


class FunctionBlockTreeView(Gtk.Window):
    def __init__(self):
        super().__init__(title="FB Treeview")
        self.set_border_width(10)

        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        self.liststore = Gtk.ListStore(str, str)
        for software_ref in software_list:
            self.liststore.append(list(software_ref))
        self.filter_language = None

        self._filter = self.liststore.filter_new()

        self._filter.set_visible_func(self._filter_func)

        self.treeview = Gtk.TreeView(model=self._filter)
        for i, column_title in enumerate(["Software", "Programming Language"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        self.treeview_selection = self.treeview.get_selection()
        self.treeview_selection.set_mode(Gtk.SelectionMode.MULTIPLE)


        self.buttons = list()
        for prog_language in ["Event Driven", "SIFB", "None"]:
            button = Gtk.Button(label=prog_language)
            self.buttons.append(button)
            button.connect("clicked", self.on_selection_button_clicked)

        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)
        self.grid.attach_next_to(self.buttons[0], self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1)

        for i, button in enumerate(self.buttons[1:]):
            self.grid.attach_next_to(button, self.buttons[i], Gtk.PositionType.RIGHT, 1, 1)
        self.scrollable_treelist.add(self.treeview)
        self.show_all()

    def _filter_func(self, model, iter, data):
        if (
                self.filter_language is None
                or self.filter_language == "None"
                ):
            return True
        else:
            return model[iter][1] == self.filter_language

    def on_selection_button_clicked(self, widget):
        """Called on any of the button clicks"""
        self.filter_language = widget.get_label()
        print("%s language selected!" % self.filter_language)
        self._filter.refilter()
        print(self._get_tree_selection())

    def _get_tree_selection(self):
        selected_function_blocks = list()
        _, tree_path_list = self.treeview_selection.get_selected_rows()

        for tree_path in tree_path_list:
            tree_iter = self.liststore.get_iter(tree_path)
            selected = self.liststore.get(tree_iter, 1)[0]
            selected_function_blocks.append(selected)
        print(selected_function_blocks)
        return selected_function_blocks


win = FunctionBlockTreeView()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
