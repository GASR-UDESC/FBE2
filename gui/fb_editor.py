import sys

import gi
from gi.repository import GLib, Gio, Gtk, GObject, Gdk

from function_block.function_block import *

from gui.fb_renderer import Function_Block_Renderer
from gui.edit_fb_combobox import EditFunctionBlockWindow
from types_and_conversions.conversions.py_xml import convert_xml_basic_fb

class MouseButtons:

    LEFT_BUTTON = 1
    RIGHT_BUTTON = 3

class Function_Block_Editor(Gtk.Box):
    def __init__(self, fb_diagram=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ref_pos = [0,0]
        self.fb_count = 0
        self.enable_add = False
        self.enable_remove =False
        self.enable_connect = False
        self.previous_selected = None
        self.selected_fb = None
        # ~ fb_diagram = world()
        self.paned = Gtk.Paned(wide_handle=True)
        self.scrolled = Gtk.ScrolledWindow.new()
        self.scrolled.set_hexpand(True)
        self.scrolled.set_vexpand(True)
        self.function_block_renderer = Function_Block_Renderer()
        self.sidebox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.frame_props = Gtk.Frame(label='Properties', visible=False, no_show_all=True)
        self.pack_start(self.paned, True, True, 0)
        self.paned.pack1(self.scrolled, True, False)
        self.scrolled.add(self.function_block_renderer)
        self.function_block_renderer.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.function_block_renderer.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK)
        self.function_block_renderer.connect("draw", self.on_draw)
        self.function_block_renderer.connect("button-press-event", self.on_button_press)
        self.function_block_renderer.connect("button-release-event", self.on_button_press)
        self.edit_fb_window = EditFunctionBlockWindow(self.selected_fb)

    def change_selected_fb(self, fb):
        self.selected_fb = fb

    def on_draw(self, wid, cr):
        for fb in self.function_block_renderer.fb_diagram.function_blocks:
            self.function_block_renderer.draw_function_block(wid, cr, fb, gain=20)
        self.function_block_renderer.draw_connections(wid, cr)

    def on_button_press(self, w, e):

        if e.type == Gdk.EventType.BUTTON_PRESS \
                and e.button == MouseButtons.LEFT_BUTTON:
                    if self.enable_add:
                        try:
                            print(self.selected_fb)
                            new_fb = convert_xml_basic_fb("types_and_conversions/types/" + self.selected_fb)
                            new_fb.pos = [e.x, e.y]
                            setattr(self.function_block_renderer.fb_diagram, "New_FB" + str(self.fb_count),new_fb)
                            self.function_block_renderer.fb_diagram.add_function_block(new_fb)
                            self.fb_count = self.fb_count + 1
                        except:
                            pass
                    else:
                        self.selected_fb, selected_event, selected_var  = self.function_block_renderer.detect_fb(e.x, e.y)
                        self.edit_fb_window.refresh(self.selected_fb)
                        self.function_block_renderer.detect_connection(e.x, e.y)
                        self.function_block_renderer.detect_fb(e.x, e.y)
                        self.ref_pos = [e.x, e.y]
                        if self.enable_remove:
                            if self.selected_fb is not None:
                                self.function_block_renderer.fb_diagram.remove_function_block(self.selected_fb)
                                self.fb_count = self.fb_count - 1
                            if self.function_block_renderer.selected_cn is not None:
                                self.function_block_renderer.selected_cn[0].connections.remove(self.function_block_renderer.selected_cn[1])
                        elif self.enable_connect:
                            if self.previous_selected == None:
                                if selected_event == None:
                                    self.previous_selected = selected_var
                                else:
                                    self.previous_selected = selected_event
                            else:
                                if selected_event is not None:
                                    self.function_block_renderer.fb_diagram.connect_events(self.previous_selected, selected_event)
                                    self.previous_selected = None
                                else:
                                    self.function_block_renderer.fb_diagram.connect_variables(self.previous_selected, selected_var)
                                    self.previous_selected = None


                    self.function_block_renderer.queue_draw()
        if e.type == Gdk.EventType.BUTTON_RELEASE:
            if self.selected_fb is not None and not self.enable_add:
                dx, dy = 0, 0
                dx, dy = (e.x - self.ref_pos[0]), (e.y - self.ref_pos[1])
                self.ref_pos = [e.x, e.y]
                self.selected_fb.change_pos(self.selected_fb.pos[0] + dx, self.selected_fb.pos[1] + dy)
                self.function_block_renderer.queue_draw()

        if e.type == Gdk.EventType.BUTTON_PRESS \
                and e.button == MouseButtons.RIGHT_BUTTON:

                    pass



