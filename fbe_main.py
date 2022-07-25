#!/usr/bin/python3

import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio
import sys
from gui.fb_editor import Function_Block_Editor
from gui.fbe_listbox import FBE_ListBox
from types_and_conversions.conversions.py_xml import *

class Window(Gtk.ApplicationWindow):
    def __init__(self, app):
        super(Window, self).__init__(title="GASR-FBE2", application=app)

        self.main_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        self.box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.main_box.pack_start(self.box, True, True, 0)

        self.menubar = Gtk.MenuBar()
        self.function_block_editor = Function_Block_Editor()
        fmi = self.create_sub_menu("File")
        self.create_simple_menu_item(fmi, Export_diagram=self.on_export_diagram, Import_Library=self.on_import_library, 
        Import_FB=self.on_import_fb, Import_diagram=self.on_import_diagram, Quit=self.quitApp)

        #nmi = self.create_sub_menu('Quit')
        #self.create_simple_menu_item(nmi, DONT_SAVE = self.quitApp)

        self.listbox = FBE_ListBox(self.function_block_editor)

        self.box.pack_start(self.menubar, False, True, 0)
        self.box.pack_start(self.function_block_editor, True, True, 0)	
        self.main_box.pack_start(self.listbox, False, False, 0)

        self.add(self.main_box)

        self.set_default_size(1000, 600)

    def quitApp(self, par):

        app.quit()    
	
    def load_function_block(self, loc):
        setattr(self.function_block_editor.function_block_renderer.fb_diagram, "New_FB_" + str(self.function_block_editor.fb_count), convert_xml_basic_fb(loc))
        self.function_block_editor.function_block_renderer.fb_diagram.add_function_block(convert_xml_basic_fb(loc))
        print(self.function_block_editor.function_block_renderer.fb_diagram.function_blocks)
        self.listbox.fb_import_list.add(loc.rsplit('/',1)[1])

    def load_diagram(self, loc):
        # ~ self.function_block_editor.fb_diagram, self.listbox.fb_import_list = import_diagram(loc)
        self.function_block_editor.function_block_renderer.fb_diagram, new_import= import_diagram(loc)
        self.listbox.fb_import_list = self.listbox.fb_import_list.union(new_import)
    def import_library(self, loc):
        directory = loc
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            if os.path.isfile(f):
                self.listbox.fb_import_list.add(f.rsplit("/",1)[1])
        
        
    def create_sub_menu(self, label):
        sub_menu = Gtk.MenuItem.new_with_label(label)
        self.menubar.add(sub_menu)
        return sub_menu

    def create_simple_menu_item(self, sub_menu, **kwargs): # kwargs are so-> label: function
        menu = Gtk.Menu()

        for label in kwargs.keys():
            label_name = label.replace("_", " ")
            menu_item = Gtk.MenuItem.new_with_label(label_name)
            try:
                menu_item.connect("activate", kwargs[label])
                menu.append(menu_item)
            except:
                menu.append(menu_item)
        sub_menu.set_submenu(menu)
	
    def on_import_fb(self, widget):
        loc = self.on_file_clicked()
        self.load_function_block(loc)
        
    def on_import_library(self, widget):
        loc = self.on_folder_clicked()
        self.import_library(loc)
                            
    def on_import_diagram(self, widget):
        loc = self.on_file_clicked()
        self.load_diagram(loc)
        
    def on_export_diagram(self, widget):
        loc = self.on_export_clicked()
        export_diagram(self.function_block_editor.function_block_renderer.fb_diagram, loc)
				
				
    def on_file_clicked(self):
        dialog = Gtk.FileChooserDialog(title="Function Block File", parent=self, action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        self.add_filters(dialog)
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog.get_filename())
            filename = dialog.get_filename()
            dialog.destroy()
            return filename
            
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
		
        dialog.destroy()
        
    def on_export_clicked(self):
        dialog = Gtk.FileChooserDialog(title="Function Block File", parent=self, action=Gtk.FileChooserAction.SAVE)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        self.add_filters(dialog)
        dialog.set_current_name("untitled.sys")
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog.get_filename())
            filename = dialog.get_filename()
            dialog.destroy()
            return filename
            
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
		
        dialog.destroy()

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        filter_py = Gtk.FileFilter()
        filter_py.set_name("Python files")
        filter_py.add_mime_type("text/x-python")
        dialog.add_filter(filter_py)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def on_folder_clicked(self):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a folder",
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK
        )
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Select clicked")
            print("Folder selected: " + dialog.get_filename())
            folder = dialog.get_filename()
            dialog.destroy()
            return folder
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()


class Application(Gtk.Application):

    def __init__(self):
        super(Application, self).__init__()

    def do_activate(self):

        self.win = Window(self)
        self.win.show_all()

    def do_startup(self):

        Gtk.Application.do_startup(self)

app = Application()
app.run(sys.argv)
