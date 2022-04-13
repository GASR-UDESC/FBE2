#!/usr/bin/python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
gi.require_version("Gtk", "3.0")
import cairo
import math
from function_block_edit import *



class MouseButtons:

    LEFT_BUTTON = 1
    RIGHT_BUTTON = 3


class Function_Block_Renderer(Gtk.Window):

    def __init__(self):
        super(Function_Block_Renderer, self).__init__()

        self.init_ui()


    def init_ui(self):    

        self.darea = Gtk.DrawingArea()
        self.darea.connect("draw", self.on_draw)
        self.darea.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)        
        self.add(self.darea)


        self.i_pos = [0,0]

        self.darea.connect("button-press-event", self.on_button_press)

        self.set_title("FBE2")
        self.resize(500, 400)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()


    def on_draw(self, wid, cr):
        print(len(self.i_pos))
        # ~ self.draw_line_conections(wid, cr)   
        for i in range(int(len(self.i_pos)/2)):
            print(self.i_pos[2*i])
            print(self.i_pos[2*i+1])
            IO_READER_1=IO_READER(INIT=False, REQ=False, QI=False, PARAMS=False, SD_1=False)
            self.draw_function_block(wid, cr, self.i_pos[2*i], self.i_pos[2*i+1], fb=IO_READER_1, gain=20)

    def draw_function_block(self, wid, cr, i_pos_x, i_pos_y, fb, gain):
        cr.set_source_rgb(0, 0, 0)
        cr.set_line_width(0.7)
        def get_fb_measurements(fb):
            in_events = list()
            out_events = list()
            in_vars = list()
            out_vars = list()
            z = list()

            for event in fb.events.keys():
                if fb.events[event].in_event:
                    in_events.append(event)
                else:
                    out_events.append(event)

            for var in fb.variables.keys():
                if fb.variables[var].in_var:
                    in_vars.append(var)
                else:
                    out_vars.append(var)

            for i in range(len(in_events)):
                try:
                    z.append(in_events[i]+out_events[i])
                except:
                    try:
                        z.append(in_events[i])
                    except:
                        z.append(out_events[i])

            for i in range(len(in_vars)):
                try:
                    z.append(in_vars[i]+out_vars[i])
                except:
                    try:
                        z.append(in_vars[i])
                    except:
                        z.append(out_vars[i])

            h_length = gain*(int(math.ceil(0.4*len(max(z, key=len))))+2)
            t_vert_length = gain*max(len(in_events), len(out_events))
            b_vert_length = gain*max(len(in_vars), len(out_vars))

            return h_length, t_vert_length, b_vert_length

        h_length, t_vert_length, b_vert_length = get_fb_measurements(fb)
        b_neck_width = h_length/6
        b_neck_height = t_vert_length/2
        print(h_length, t_vert_length, b_vert_length)


        cr.move_to(i_pos_x, i_pos_y)
        cr.line_to(i_pos_x, i_pos_y + t_vert_length)
        cr.move_to(i_pos_x, i_pos_y + t_vert_length)
        cr.line_to(i_pos_x + b_neck_width, i_pos_y + t_vert_length)
        cr.move_to(i_pos_x + b_neck_width, i_pos_y + t_vert_length)
        cr.line_to(i_pos_x + b_neck_width, i_pos_y + t_vert_length + b_neck_height)
        cr.move_to(i_pos_x + b_neck_width, i_pos_y + t_vert_length + b_neck_height)
        cr.line_to(i_pos_x, i_pos_y + t_vert_length + b_neck_height)
        cr.move_to(i_pos_x, i_pos_y + t_vert_length + b_neck_height)
        cr.line_to(i_pos_x, i_pos_y + t_vert_length + b_neck_height + b_vert_length)
        cr.move_to(i_pos_x, i_pos_y + t_vert_length + b_neck_height + b_vert_length)
        cr.line_to(i_pos_x + h_length, i_pos_y + t_vert_length + b_neck_height + b_vert_length) 
        cr.move_to(i_pos_x + h_length, i_pos_y + t_vert_length + b_neck_height + b_vert_length)
        cr.line_to(i_pos_x + h_length, i_pos_y + t_vert_length + b_neck_height)
        cr.move_to(i_pos_x + h_length, i_pos_y + t_vert_length + b_neck_height)
        cr.line_to(i_pos_x + h_length - b_neck_width, i_pos_y + t_vert_length + b_neck_height)
        cr.move_to(i_pos_x + h_length - b_neck_width, i_pos_y + t_vert_length + b_neck_height)
        cr.line_to(i_pos_x + h_length - b_neck_width, i_pos_y + t_vert_length)
        cr.move_to(i_pos_x + h_length - b_neck_width, i_pos_y + t_vert_length)
        cr.line_to(i_pos_x + h_length, i_pos_y + t_vert_length)
        cr.move_to(i_pos_x + h_length, i_pos_y + t_vert_length)
        cr.line_to(i_pos_x + h_length, i_pos_y)
        cr.move_to(i_pos_x + h_length, i_pos_y)
        cr.line_to(i_pos_x, i_pos_y)
        cr.stroke()
        self.write_txt(wid, cr, "E_SMTHNG", i_pos_x + b_neck_width, i_pos_y+t_vert_length+b_neck_height/2)
        i=0
        j=0
        for event in fb.events.keys():
            if fb.events[event].in_event:
                self.write_txt(wid, cr, event, i_pos_x, 12 + i_pos_y + i*gain)
                i = i+1 
            else:
                self.write_txt(wid, cr, event, i_pos_x + h_length - 7*len(event), 12 + i_pos_y + j*gain)
                j = j+1

        i=0
        j=0
        for var in fb.variables.keys():
            if fb.variables[var].in_var:
                self.write_txt(wid, cr, var, i_pos_x, 12 + i_pos_y + i*gain + t_vert_length + b_neck_height)
                i = i+1 
            else:
                self.write_txt(wid, cr, var, i_pos_x + h_length - 7*len(var), 12 + i_pos_y + j*gain + t_vert_length + b_neck_height)
                j = j+1

    def write_txt(self, wid, cr, name, i_pos_x, i_pos_y):
        cr.set_source_rgb(0, 0, 0)
        cr.select_font_face('Courier', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(12)
        cr.move_to(i_pos_x, i_pos_y)
        cr.show_text(name)

    def on_button_press(self, w, e):

        if e.type == Gdk.EventType.BUTTON_PRESS \
                and e.button == MouseButtons.LEFT_BUTTON:

                    self.i_pos.append(e.x)
                    self.i_pos.append(e.y)
                    self.darea.queue_draw()  

        if e.type == Gdk.EventType.BUTTON_PRESS \
                and e.button == MouseButtons.RIGHT_BUTTON:

                    self.darea.queue_draw()           


def main():

    app = Function_Block_Renderer()
    Gtk.main()


if __name__ == "__main__":    
    main()
