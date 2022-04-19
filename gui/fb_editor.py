import sys
import gi
from gi.repository import GLib, Gio, Gtk, GObject, Gdk

from function_block_edit import *

from fb_renderer import Function_Block_Renderer

class MouseButtons:

    LEFT_BUTTON = 1
    RIGHT_BUTTON = 3

class Function_Block_Editor(Gtk.Box):
    def __init__(self, function_block=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.function_block = function_block
        self.paned = Gtk.Paned(wide_handle=True)
        self.scrolled = Gtk.ScrolledWindow.new()
        self.function_block_renderer = Function_Block_Renderer(self.function_block)
        self.sidebox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.frame_props = Gtk.Frame(label='Properties', visible=False, no_show_all=True)
        self.pack_start(self.paned, True, True, 0)
        self.paned.pack1(self.scrolled, True, False)
        self.paned.pack2(self.sidebox, False, False)
        self.scrolled.add(self.function_block_renderer)
        self.function_block_renderer.set_events(Gdk.EventMask.BUTTON_PRESS_MASK) 
        self.function_block_renderer.connect("draw", self.on_draw)
        self.function_block_renderer.connect("button-press-event", self.on_button_press)


    def on_draw(self, wid, cr):
        # ~ self.draw_line_conections(wid, cr)   
        for i in range(int(len(self.function_block_renderer.i_pos)/2)):
            IO_READER_1=IO_READER(INIT=False, REQ=False, QI=False, PARAMS=False, SD_1=False)
            E_PERMIT = PERMIT(EI=False, PERMIT=False)
            DELAY = E_RESTART(COLD=False, WARM=False, STOP=False)
            self.function_block_renderer.draw_function_block(wid, cr, self.function_block_renderer.i_pos[2*i], self.function_block_renderer.i_pos[2*i+1], fb=E_PERMIT, gain=20)

    def on_button_press(self, w, e):

        if e.type == Gdk.EventType.BUTTON_PRESS \
                and e.button == MouseButtons.LEFT_BUTTON:
                    self.function_block_renderer.i_pos.append(e.x)
                    self.function_block_renderer.i_pos.append(e.y)
                    self.function_block_renderer.queue_draw()  

        if e.type == Gdk.EventType.BUTTON_PRESS \
                and e.button == MouseButtons.RIGHT_BUTTON:

                    pass



