import sys

import gi
from gi.repository import GLib, Gio, Gtk, GObject, Gdk

from function_block.function_block import *

from gui.fb_renderer import Function_Block_Renderer


class MouseButtons:

    LEFT_BUTTON = 1
    RIGHT_BUTTON = 3

class Function_Block_Editor(Gtk.Box):
    def __init__(self, fb_diagram=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ref_pos = [0,0]
        self.enable_add = False
        self.enable_remove =False
        self.enable_connect = False
        self.previous_selected = None
        self.selected_fb = None
        self.fb_diagram = world()
        self.paned = Gtk.Paned(wide_handle=True)
        self.scrolled = Gtk.ScrolledWindow.new()
        self.scrolled.set_hexpand(True)
        self.scrolled.set_vexpand(True)
        self.function_block_renderer = Function_Block_Renderer(self.fb_diagram)
        self.sidebox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.frame_props = Gtk.Frame(label='Properties', visible=False, no_show_all=True)
        self.pack_start(self.paned, True, True, 0)
        self.paned.pack1(self.scrolled, True, False)
        self.paned.pack2(self.sidebox, False, False)
        self.scrolled.add(self.function_block_renderer)
        self.function_block_renderer.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.function_block_renderer.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK)
        self.function_block_renderer.connect("draw", self.on_draw)
        self.function_block_renderer.connect("button-press-event", self.on_button_press)
        self.function_block_renderer.connect("button-release-event", self.on_button_press)

    def change_selected_fb(self, fb):
        self.selected_fb = fb

    def on_draw(self, wid, cr):
        # ~ self.draw_line_conections(wid, cr)   
        for fb in self.fb_diagram.function_blocks:
            self.function_block_renderer.draw_function_block(wid, cr, fb, gain=20)

    def on_button_press(self, w, e):

        if e.type == Gdk.EventType.BUTTON_PRESS \
                and e.button == MouseButtons.LEFT_BUTTON:
                    if self.enable_add:
                        self.fb_diagram.new_function_block("fb" + str(len(self.fb_diagram.function_blocks)), self.selected_fb)
                        getattr(self.fb_diagram, "fb" + str(len(self.fb_diagram.function_blocks)-1)).pos = [e.x, e.y]  

                    else:
                        self.selected_fb, selected_event, selected_var  = self.function_block_renderer.detect_fb(self.fb_diagram, e.x, e.y)
                        print(self.function_block_renderer.detect_fb(self.fb_diagram, e.x, e.y))
                        self.ref_pos = [e.x, e.y]
                        if self.enable_remove:
                            self.fb_diagram.remove_function_block(self.selected_fb)
                        elif self.enable_connect:
                            if self.previous_selected == None:
                                try:	
                                    self.previous_selected = selected_event
                                except:
                                    self.previous_selected = selected_var
                            else:
                                try:
                                    self.fb_diagram.connect_events(self.previous_selected, selected_event)
                                except:
                                    self.fb_diagram.connect_variables(self.previous_selected, selected_var)
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



