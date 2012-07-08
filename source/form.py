#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 Deepin, Inc.
#               2012 Hailong Qiu
#
# Author:     Hailong Qiu <356752238@qq.com>
# Maintainer: Hailong Qiu <356752238@qq.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gtk
from skin           import app_theme

from dtk.ui.button import Button



#############
# Form 123456
#############
class Form(gtk.Fixed):
    def __init__(self):
        gtk.Fixed.__init__(self)
        self.set_size_request(200, 200)
        self.width  = 200
        self.height = 200
        self.x      = 0
        self.y      = 0
        self.text   = "Form"
        
        self.press_bool = False
        self.motion_bool = False
        # Init events.
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.connect("button-press-event", self.button_press_event)
        self.connect("motion-notify-event", self.button_press_event)
        self.connect("expose-event", self.draw_form_background)
        
    def size(self, width, height):    
        self.width   = width
        self.height  = height
        self.set_size_request(width, height)
        
    def move(self, x, y):    
        self.x = x
        self.y = y                
        
    def button_press_event(self, widget, event):    
        print event.x
        
    def draw_form_background(self, widget, event):
        cr = widget.window.cairo_create()
        x, y, width, height = widget.allocation
        self.draw_background(cr, x, y)
        
        self.draw_left_rectangle(cr,   x, y)
        self.draw_bottom_rectangle(cr, x, y)
        self.draw_rangl_rectangle(cr,  x, y)
        
    def draw_rectangle(self, cr, x, y, w, h):
        cr.set_source_rgb(1, 1, 1)
        cr.rectangle(x, y, w, h)
        cr.fill()
        
        cr.set_source_rgb(0, 0, 0)
        cr.rectangle(x, y, w, h)
        cr.stroke()
        

    def draw_bottom_rectangle(self, cr, x, y):    
        w = 5
        h = 5
        self.draw_rectangle(cr, 
                            x + (self.x + self.width)/2, 
                            y + (self.y + self.height - h/2),
                            w, h)
    
    def draw_left_rectangle(self, cr, x, y):
        w = 5
        h = 5
        self.draw_rectangle(cr,
                            x + (self.x + self.width - w/2),
                            y + (self.y + self.height)/2,
                            w, h)
        
    def draw_rangl_rectangle(self, cr, x, y):
        w = 5
        h = 5
        self.draw_rectangle(cr,
                            x + (self.x + self.width - w/2),
                            y + (self.y + self.height - h/2),
                            w, h)
    
    def draw_background(self, cr, x, y):
        # Draw backround.
        window_bg_pixbuf = gtk.gdk.pixbuf_new_from_file("image/window_bg.png")
        window_bg_image  = window_bg_pixbuf.scale_simple(self.width, self.height, gtk.gdk.INTERP_BILINEAR)
        alpha = 1                
        cr.set_source_pixbuf(window_bg_image, x + self.x, y + self.y)
        cr.paint_with_alpha(alpha)
        # Draw point.
        for x_padding in range(5, self.width - 3, 5):
            for y_pdding in range(5, self.height - 3, 5):
                self.draw_rectangle(cr, x + self.x + x_padding, y + self.y + y_pdding, 0.2, 0.2)

class widget(object):
    def __init__(self):
        self.width  = 200
        self.height = 200
        self.x      = 0
        self.y      = 0
        self.text   = "Form"
        self.press_bool = False
        self.motion_bool = False
        global stack_num
        global max_stack_num
        global min_stack_num
        self.stack_num   = stack_num
        stack_num += 1
        max_stack_num = stack_num
        
    def size(self, width, height):    
        self.width   = width
        self.height  = height
        
    def move(self, x, y):    
        self.x = x
        self.y = y        
        
    def set_above(self, bool):
        if bool:
            global stack_num
            global max_stack_num
            stack_num = max_stack_num + 1
            max_stack_num = stack_num
            self.stack_num = stack_num
        # else:    
        #     stack_num = min_stack_num - 1
        #     min_stack_num = stack_num
        #     self.stack_num = stack_num
            
    def draw_widget(self, widget, event):
        cr = widget.window.cairo_create()
        x, y, width, height = widget.allocation
        self.draw_background(cr, x, y)
        
        self.draw_left_rectangle(cr,   x, y)
        self.draw_bottom_rectangle(cr, x, y)
        self.draw_rangl_rectangle(cr,  x, y)
        
    def draw_rectangle(self, cr, x, y, w, h):    
        cr.set_source_rgb(1, 1, 1)
        cr.rectangle(x, y, w, h)
        cr.fill()
        
        cr.set_source_rgb(0, 0, 0)
        cr.rectangle(x, y, w, h)        
        cr.stroke()
        
        

    def draw_bottom_rectangle(self, cr, x, y):    
        w = 5
        h = 5
        self.draw_rectangle(cr, 
                            x + (self.x + self.width)/2, 
                            y + (self.y + self.height - h/2),
                            w, h)
    
    def draw_left_rectangle(self, cr, x, y):
        w = 5
        h = 5
        self.draw_rectangle(cr,
                            x + (self.x + self.width - w/2),
                            y + (self.y + self.height)/2,
                            w, h)
        
    def draw_rangl_rectangle(self, cr, x, y):
        w = 5
        h = 5
        self.draw_rectangle(cr,
                            x + (self.x + self.width - w/2),
                            y + (self.y + self.height - h/2),
                            w, h)
    
    def draw_background(self, cr, x, y):
        # Draw backround.
        window_bg_pixbuf = gtk.gdk.pixbuf_new_from_file("image/window_bg.png")
        window_bg_image  = window_bg_pixbuf.scale_simple(self.width, self.height, gtk.gdk.INTERP_BILINEAR)
        alpha = 1                
        cr.set_source_pixbuf(window_bg_image, x + self.x, y + self.y)
        cr.paint_with_alpha(alpha)
        # Draw point.
        for x_padding in range(5, self.width - 3, 5):
            for y_pdding in range(5, self.height - 3, 5):
                self.draw_rectangle(cr, x + self.x + x_padding, y + self.y + y_pdding, 0.2, 0.2)
    
                
widgets = []    
stack_num = 0
max_stack_num = 0
min_stack_num = 0

def BUTTON_PRESS_EVENT(event, other_events):
    other_events_bool = True
    
    for w in widgets:
        if w.x <= event.x <= w.x + w.width and w.y <= event.y <= w.y + w.height:
            w.press_bool = True
            other_events_bool = False
        
    if other_events_bool:            
        for o_es in other_events:
            o_es()
        
    if len(widgets) > 1:        
        temp_widgets = []
        for w in widgets:
            if w.press_bool:
                temp_widgets.append(w)
                    
        if len(temp_widgets) > 1:
            if temp_widgets:        
                    max_widget = temp_widgets[0]
            
            for w in temp_widgets:
                if w.stack_num > max_widget.stack_num:            
                    max_widget = w
                else:       
                    w.press_bool = False
                        
            if max_widget.stack_num == temp_widgets[0].stack_num:
                temp_widgets[0].press_bool = True
                   
    for w in widgets:        
        if w.press_bool:
            print w.text
                
    for w in widgets:        
        w.press_bool = False

def MOTION_NOTIFY_EVENT(event, other_events):        
    other_events_bool = True    
    
    for w in widgets:
        if w.x <= event.x <= w.x + w.width and w.y <= event.y <= w.y + w.height:
            w.motion_bool = True
            other_events_bool = False
            
    if other_events_bool:                    
        for o_es in other_events:
            o_es()
                
    if len(widgets) > 1:        
        temp_widgets = []
        for w in widgets:
            if w.motion_bool:
                temp_widgets.append(w)
                    
        if len(temp_widgets) > 1:
            if temp_widgets:        
                    max_widget = temp_widgets[0]
            
            for w in temp_widgets:
                if w.stack_num > max_widget.stack_num:            
                    max_widget = w
                else:       
                    w.motion_bool = False
                        
            if max_widget.stack_num == temp_widgets[0].stack_num:
                temp_widgets[0].motion_bool = True
                   
    for w in widgets:        
        if w.motion_bool:
            print w.text
                
    for w in widgets:        
        w.motion_bool = False
        
        
def DRAW_ALL_WIDGET(widget, event):            
    for w in widgets:
        w.draw_widget(widget, event)

        
################        
# Window class. 123456               
################        
class Window(gtk.Window):
    def __init__(self, window_type=gtk.WINDOW_TOPLEVEL):
        gtk.Window.__init__(self, window_type)
        
        
        # Init set window.
        self.set_title("python可视化开发环境")
        self.set_size_request(700, 500)
        
        self.main_fixed = gtk.Fixed()
        self.form_fixed = gtk.Fixed()
        self.form_fixed.connect("expose-event", self.draw_widgets)        
        # Init form window.
        self.form = Form()
        self.form_fixed.set_size_request(500, 500)                
        self.form_fixed.put(self.form, 0, 0)
        self.main_fixed.put(self.form_fixed, 100, 100)
        
        self.form.put(Button("确定"), 50, 50)
        self.add(self.main_fixed)
        
    def add_widget(self, widget):
        widgets.append(widget)        
        
    def draw_widgets(self, widget, event):
        cr = widget.window.cairo_create()
        x, y, w, h = widget.allocation
        r = g = b = 0.4
        cr.set_source_rgb(r, g, b)
        cr.rectangle(x, y, w, h)
        cr.fill()
        
    
    
if __name__ == "__main__":
    def draw_widgets(widget, event):        
        DRAW_ALL_WIDGET(widget, event)
        return True
            
    def printstring(widget, event):
        print widget
        print event.x
        
    def button_press_event(widget, event):        
        # 
        other_events = [lambda :printstring(widget, event),
                        lambda :widgets[0].move(event.x, event.y)]
        BUTTON_PRESS_EVENT(event, other_events)
        # MOTION_NOTIFY_EVENT(event, other_events)
        
    win = Window(gtk.WINDOW_TOPLEVEL)    
    
    win.add_events(gtk.gdk.ALL_EVENTS_MASK)
    # win.connect("destory", gtk.main_quit)
    win.connect("expose-event", draw_widgets)
    win.connect("button-press-event", button_press_event)
    # win.connect("motion-notify-event", button_press_event)
    form1 = Form()
    form2 = Form()
    form3 = Form()
    
    win.add(form1)
    win.add(form2)
    win.add(form3)
    
    form1.move(200, 200)
    form2.move(80, 80)
    form3.move(100, 100)
    form1.text = "window1"
    form2.text = "testwin2"
    form3.text = "window333333"
    form1.size(500, 500)
    form1.set_above(True)
    
    win.show_all()
        
    gtk.main()
    
