#!/usr/bin/python3
import sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
gi.require_version("Gtk", "3.0")
import cairo
import math
from function_block.function_block import *


class Function_Block_Renderer(Gtk.DrawingArea):
    def __init__(self, fb_diagram=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fb_diagram = fb_diagram

    def draw_function_block(self, wid, cr, fb, gain):
        cr.set_source_rgb(0, 0, 0)
        cr.set_line_width(0.7)
        if fb.selected:
            cr.set_source_rgb(1, 0, 0)
            cr.set_line_width(1)

        i_pos_x = fb.pos[0]
        i_pos_y = fb.pos[1]


        h_length, t_vert_length, b_vert_length = self.get_fb_measurements(fb, gain)
        b_neck_width = h_length/6
        b_neck_height = t_vert_length/2
        #print(h_length, t_vert_length, b_vert_length)


        cr.move_to(i_pos_x, i_pos_y)
        cr.line_to(i_pos_x, i_pos_y + t_vert_length)
        cr.line_to(i_pos_x + b_neck_width, i_pos_y + t_vert_length)
        cr.line_to(i_pos_x + b_neck_width, i_pos_y + t_vert_length + b_neck_height)
        cr.line_to(i_pos_x, i_pos_y + t_vert_length + b_neck_height)
        cr.line_to(i_pos_x, i_pos_y + t_vert_length + b_neck_height + b_vert_length)
        cr.line_to(i_pos_x + h_length, i_pos_y + t_vert_length + b_neck_height + b_vert_length) 
        cr.line_to(i_pos_x + h_length, i_pos_y + t_vert_length + b_neck_height)
        cr.line_to(i_pos_x + h_length - b_neck_width, i_pos_y + t_vert_length + b_neck_height)
        cr.line_to(i_pos_x + h_length - b_neck_width, i_pos_y + t_vert_length)
        cr.line_to(i_pos_x + h_length, i_pos_y + t_vert_length)
        cr.line_to(i_pos_x + h_length, i_pos_y)
        cr.line_to(i_pos_x, i_pos_y)
        cr.stroke()

        self.write_txt(wid, cr, fb.name, i_pos_x + h_length/2-(7*len(fb.name)/2), gain + i_pos_y+t_vert_length+b_neck_height/2)

        i=0
        j=0
        for event in fb.events.keys():
            if fb.events[event].in_event:
                self.write_txt(wid, cr, event, i_pos_x, 12 + i_pos_y + i*gain, selected=fb.events[event].selected)
                fb.events[event].pos = [i_pos_x, 12 + i_pos_y + i*gain]
                i = i+1 
            else:
                self.write_txt(wid, cr, event, i_pos_x + h_length - 7*len(event), 12 + i_pos_y + j*gain, selected=fb.events[event].selected)
                fb.events[event].pos = [i_pos_x + h_length - 7*len(event), 12 + i_pos_y + j*gain]
                j = j+1

        i=0
        j=0
        for var in fb.variables.keys():
            if fb.variables[var].in_var:
                self.write_txt(wid, cr, var, i_pos_x, 12 + i_pos_y + i*gain + t_vert_length + b_neck_height + gain, selected=fb.variables[var].selected)
                fb.variables[var].pos = [i_pos_x, 12 + i_pos_y + i*gain + t_vert_length + b_neck_height + gain]
                i = i+1 
            else:
                self.write_txt(wid, cr, var, i_pos_x + h_length - 7*len(var), 12 + i_pos_y + j*gain + t_vert_length + b_neck_height + gain, selected=fb.variables[var].selected)
                fb.variables[var].pos = [i_pos_x + h_length - 7*len(var), 12 + i_pos_y + j*gain + t_vert_length + b_neck_height + gain]
                j = j+1

    def draw_connections(self, wid, cr, gain=20, selected=0):
        cr.set_source_rgb(selected, 0, 0)
        i = 0
        for fb in self.fb_diagram.function_blocks:
            for var in fb.variables.items():
                for connection in var[1].connections:
                    h_length, t_vert_length, b_vert_length = self.get_fb_measurements(var[1].block, gain=20)
                    if var[1].pos[0] > connection.pos[0]:
                        i = i + 1
                        cr.move_to(var[1].block.pos[0] + h_length, var[1].pos[1])
                        cr.line_to(len(var[0])*7 + var[1].block.pos[0] + h_length, var[1].pos[1])
                        if var[1].pos[1] < connection.pos[1]:
                            h_length, t_vert_length, b_vert_length = self.get_fb_measurements(connection.block, gain=20)
                            cr.line_to(len(var[0])*7 + var[1].block.pos[0] + h_length, connection.block.pos[1] + t_vert_length + b_vert_length + t_vert_length/2 + gain/(i))
                            cr.line_to(connection.block.pos[0] - len(var[0])*7, connection.block.pos[1] + t_vert_length + b_vert_length + t_vert_length/2 + gain/(i))
                        else:
                            cr.line_to(len(var[0])*7 + var[1].block.pos[0] + h_length, var[1].block.pos[1] + t_vert_length + b_vert_length + t_vert_length/2 + gain/(i))
                            cr.line_to(connection.block.pos[0] - len(var[0])*7, var[1].block.pos[1] + t_vert_length + b_vert_length + t_vert_length/2 + gain/(i))

                        cr.line_to(connection.block.pos[0] - len(var[0])*7, connection.pos[1])
                        cr.line_to(connection.pos[0], connection.pos[1])

                    else:
                        cr.move_to(var[1].block.pos[0] + h_length, var[1].pos[1])
                        cr.line_to((connection.block.pos[0] - var[1].block.pos[0] - h_length)/2 + var[1].block.pos[0] + h_length, var[1].pos[1])
                        cr.line_to((connection.block.pos[0]- var[1].block.pos[0] - h_length)/2 + var[1].block.pos[0] + h_length, connection.pos[1])
                        cr.line_to(connection.block.pos[0], connection.pos[1])
                cr.stroke()
            i = 0
            for event in fb.events.items():
                for connection in event[1].connections:
                    h_length, _, _ = self.get_fb_measurements(event[1].block, gain=20)
                    if event[1].pos[0] > connection.pos[0]:
                        i = i + 1
                        cr.move_to(event[1].block.pos[0] + h_length, event[1].pos[1])
                        cr.line_to(len(event[0])*7 + event[1].block.pos[0] + h_length, event[1].pos[1])
                        if event[1].pos[1] < connection.pos[1]:
                            cr.line_to(len(event[0])*7 + event[1].block.pos[0] + h_length, event[1].block.pos[1] - gain/i)
                            cr.line_to(connection.block.pos[0] - len(event[0])*7, event[1].block.pos[1] -gain/i)
                        else:
                            cr.line_to(len(event[0])*7 + event[1].block.pos[0] + h_length, connection.block.pos[1] - gain/i)
                            cr.line_to(connection.block.pos[0] - len(event[0])*7, connection.block.pos[1] -gain/i)

                        cr.line_to(connection.block.pos[0] - len(event[0])*7, connection.pos[1])
                        cr.line_to(connection.pos[0], connection.pos[1])

                    else:
                        cr.move_to(event[1].block.pos[0] + h_length, event[1].pos[1])
                        cr.line_to((connection.block.pos[0] - event[1].block.pos[0] - h_length)/2 + event[1].block.pos[0] + h_length, event[1].pos[1])
                        cr.line_to((connection.block.pos[0]- event[1].block.pos[0] - h_length)/2 + event[1].block.pos[0] + h_length, connection.pos[1])
                        cr.line_to(connection.block.pos[0], connection.pos[1])
                cr.stroke()


    def write_txt(self, wid, cr, name, i_pos_x, i_pos_y, selected=0):
        cr.set_source_rgb(selected, 0, 0)
        cr.select_font_face('Courier', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(12)
        cr.move_to(i_pos_x, i_pos_y)
        cr.show_text(name)

    def detect_fb(self, x, y):
        selected_fb = None
        selected_event = None
        selected_var = None

        for fb in self.fb_diagram.function_blocks:
            h_length, t_vert_length, b_vert_length = self.get_fb_measurements(fb, gain=20)
            b_neck_height = t_vert_length/2
            if (x - h_length) <= fb.pos[0] and (y - t_vert_length - b_neck_height - b_vert_length) <= fb.pos[1] and x >= fb.pos[0] and y >= fb.pos[1]:
                selected_fb = fb
                fb.selected = True
            else:
                fb.selected = False

        if selected_fb is not None:
            for event in selected_fb.events.items():
                obj_length = 7*len(event[0])
                obj_height = 12
                if (x-obj_length) <= event[1].pos[0] and (y+obj_height) >= event[1].pos[1] and x >= event[1].pos[0] and y <= event[1].pos[1]:
                    selected_event = event[1]
                    event[1].selected = 1
                else:
                    event[1].selected = 0

            if selected_event == None:
                for var in selected_fb.variables.items():
                    obj_length = 7*len(var[0])
                    obj_height = 12
                    if (x-obj_length) <= var[1].pos[0] and (y+obj_height) >= var[1].pos[1] and x >= var[1].pos[0] and y <= var[1].pos[1]:
                        selected_var = var[1]
                        var[1].selected = 1
                    else:
                        var[1].selected = 0


        return selected_fb, selected_event, selected_var

    def detect_connection(self, x, y, z=7):
        selected_cn = None
        for fb in self.fb_diagram.function_blocks:
            for event in fb.events.items():
                for connection in event[1].connections:
                    h_length,_,_ = self.get_fb_measurements(event[1].block, gain=20)
                    mid = (connection.pos[0] - event[1].block.pos[0] - h_length)/2 + event[1].block.pos[0] + h_length
                    if x<mid and x>event[1].pos[0]:
                        if  y<(event[1].pos[1] + z) and y>(event[1].pos[1]-z):
                            selected_cn = (event[1], connection)
                    elif x<(mid+z) and x>(mid-z):
                        if event[1].pos[1] < connection.pos[1]:
                            if y>=event[1].pos[1] and y<=connection.pos[1]:
                                selected_cn = (event[1], connection)
                        else:
                            if y<=event[1].pos[1] and y>=connection.pos[1]:
                                selected_cn = (event[1], connection)
                    elif x>mid and x<connection.pos[0]:
                        if y>=event[1].pos[1] and y<=connection.pos[1]:
                            selected_cn = (event[1], connection)
        return selected_cn

    def get_fb_measurements(self, fb, gain):
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




