#!/usr/bin/python3
import sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
gi.require_version("Gtk", "3.0")
import cairo
import math
from function_block import *


class Function_Block_Renderer(Gtk.DrawingArea):
    def __init__(self, fb_diagram=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fb_diagram = fb_diagram
    
    def draw_function_block(self, wid, cr, fb, gain):
        cr.set_source_rgb(0, 0, 0)
        cr.set_line_width(0.7)
        
        i_pos_x = fb.pos[0]
        i_pos_y = fb.pos[1]

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
            if len(in_events) == 0:
                for i in range(len(out_events)):
                    z.append(out_events[i])
            for i in range(len(in_vars)):
                try:
                    z.append(in_vars[i]+out_vars[i])
                except:
                    try:
                        z.append(in_vars[i])
                    except:
                        z.append(out_vars[i])
            if len(in_vars) == 0:
                for i in range(len(out_vars)):
                    z.append(out_vars[i])
           # print(z)
            h_length = gain*(int(math.ceil(0.2*len(max(z, key=len))))+2)
            t_vert_length = gain*max(len(in_events), len(out_events))
            b_vert_length = gain*(max(len(in_vars), len(out_vars))+1)

            return h_length, t_vert_length, b_vert_length

        h_length, t_vert_length, b_vert_length = get_fb_measurements(fb)
        b_neck_width = h_length/6
        b_neck_height = t_vert_length/2
        #print(h_length, t_vert_length, b_vert_length)


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

        self.write_txt(wid, cr, fb.name, i_pos_x + h_length/2-(7*len(fb.name)/2), gain + i_pos_y+t_vert_length+b_neck_height/2)

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
                self.write_txt(wid, cr, var, i_pos_x, 12 + i_pos_y + i*gain + t_vert_length + b_neck_height + gain)
                i = i+1 
            else:
                self.write_txt(wid, cr, var, i_pos_x + h_length - 7*len(var), 12 + i_pos_y + j*gain + t_vert_length + b_neck_height + gain)
                j = j+1

    def write_txt(self, wid, cr, name, i_pos_x, i_pos_y):
        cr.set_source_rgb(0, 0, 0)
        cr.select_font_face('Courier', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(12)
        cr.move_to(i_pos_x, i_pos_y)
        cr.show_text(name)

   




