#!/usr/bin/python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
gi.require_version("Gtk", "3.0")
import cairo


class MouseButtons:

    LEFT_BUTTON = 1
    RIGHT_BUTTON = 3


class Example(Gtk.Window):

    def __init__(self):
        super(Example, self).__init__()

        self.init_ui()


    def init_ui(self):    

        self.darea = Gtk.DrawingArea()
        self.darea.connect("draw", self.on_draw)
        self.darea.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)        
        self.add(self.darea)

        self.coords = []
        self.i_pos = [0,0]

        self.darea.connect("button-press-event", self.on_button_press)

        self.set_title("Lines")
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
            self.draw_function_block(wid, cr, self.i_pos[2*i], self.i_pos[2*i+1])

    def draw_line_conections(self, wid, cr):
        cr.set_source_rgb(0, 0, 0)
        cr.set_line_width(0.5)

        for i in self.coords:
            for j in self.coords:

                cr.move_to(i[0], i[1])
                cr.line_to(j[0], j[1]) 
                cr.stroke()

        del self.coords[:] 

    def draw_function_block(self, wid, cr, i_pos_x, i_pos_y):
        cr.set_source_rgb(0, 0, 0)
        cr.set_line_width(0.5)
        print("I ran")
        h_length = 12*5
        b_vert_length = 12*5
        b_neck_width = h_length/6
        b_neck_height = 4*5
        t_vert_length = 8*5


        cr.move_to(i_pos_x, i_pos_y)
        cr.line_to(i_pos_x, i_pos_y + b_vert_length)
        cr.move_to(i_pos_x, i_pos_y + b_vert_length)
        cr.line_to(i_pos_x + b_neck_width, i_pos_y + b_vert_length)
        cr.move_to(i_pos_x + b_neck_width, i_pos_y + b_vert_length)
        cr.line_to(i_pos_x + b_neck_width, i_pos_y + b_vert_length + b_neck_height)
        cr.move_to(i_pos_x + b_neck_width, i_pos_y + b_vert_length + b_neck_height)
        cr.line_to(i_pos_x, i_pos_y + b_vert_length + b_neck_height)
        cr.move_to(i_pos_x, i_pos_y + b_vert_length + b_neck_height)
        cr.line_to(i_pos_x, i_pos_y + b_vert_length + b_neck_height + t_vert_length)
        cr.move_to(i_pos_x, i_pos_y + b_vert_length + b_neck_height + t_vert_length)
        cr.line_to(i_pos_x + h_length, i_pos_y + b_vert_length + b_neck_height + t_vert_length) 
        cr.move_to(i_pos_x + h_length, i_pos_y + b_vert_length + b_neck_height + t_vert_length)
        cr.line_to(i_pos_x + h_length, i_pos_y + b_vert_length + b_neck_height)
        cr.move_to(i_pos_x + h_length, i_pos_y + b_vert_length + b_neck_height)
        cr.line_to(i_pos_x + h_length - b_neck_width, i_pos_y + b_vert_length + b_neck_height)
        cr.move_to(i_pos_x + h_length - b_neck_width, i_pos_y + b_vert_length + b_neck_height)
        cr.line_to(i_pos_x + h_length - b_neck_width, i_pos_y + b_vert_length)
        cr.move_to(i_pos_x + h_length - b_neck_width, i_pos_y + b_vert_length)
        cr.line_to(i_pos_x + h_length, i_pos_y + b_vert_length)
        cr.move_to(i_pos_x + h_length, i_pos_y + b_vert_length)
        cr.line_to(i_pos_x + h_length, i_pos_y)
        cr.move_to(i_pos_x + h_length, i_pos_y)
        cr.line_to(i_pos_x, i_pos_y)
        cr.stroke()

    def on_button_press(self, w, e):

        if e.type == Gdk.EventType.BUTTON_PRESS \
                and e.button == MouseButtons.LEFT_BUTTON:

                    self.coords.append([e.x, e.y])
                    self.i_pos.append(e.x)
                    self.i_pos.append(e.y)
                    self.darea.queue_draw()  

        if e.type == Gdk.EventType.BUTTON_PRESS \
                and e.button == MouseButtons.RIGHT_BUTTON:

                    self.darea.queue_draw()           


def main():

    app = Example()
    Gtk.main()


if __name__ == "__main__":    
    main()
