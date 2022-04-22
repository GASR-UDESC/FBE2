import sys

import gi
from gi.repository import GLib, Gio, Gtk, GObject, Gdk

from function_block import *

from fb_renderer import Function_Block_Renderer

class MouseButtons:

    LEFT_BUTTON = 1
    RIGHT_BUTTON = 3

class Function_Block_Editor(Gtk.Box):
    def __init__(self, fb_diagram=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.enable_add = False
        self.selected_fb = None
        self.fb_diagram = world()
        self.paned = Gtk.Paned(wide_handle=True)
        self.scrolled = Gtk.ScrolledWindow.new()
        self.function_block_renderer = Function_Block_Renderer(self.fb_diagram)
        self.sidebox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.frame_props = Gtk.Frame(label='Properties', visible=False, no_show_all=True)
        self.pack_start(self.paned, True, True, 0)
        self.paned.pack1(self.scrolled, True, False)
        self.paned.pack2(self.sidebox, False, False)
        self.scrolled.add(self.function_block_renderer)
        self.function_block_renderer.set_events(Gdk.EventMask.BUTTON_PRESS_MASK) 
        self.function_block_renderer.connect("draw", self.on_draw)
        self.function_block_renderer.connect("button-press-event", self.on_button_press)

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
                        self.function_block_renderer.queue_draw()  

        if e.type == Gdk.EventType.BUTTON_PRESS \
                and e.button == MouseButtons.RIGHT_BUTTON:

                    pass



