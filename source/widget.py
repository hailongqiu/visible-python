#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 SANGUO, Inc.
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
from tool import draw_background, draw_press_rectangle, all_widget



class Button(gtk.Button):
    def __init__(self):
        gtk.Button.__init__(self)
        self.press_bool = False
        self.set_size_request(120, 30)
        
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.connect("expose-event", self.draw_button)
        self.connect("button-press-event", self.button_press_event)

    def button_press_event(self, widget, event):    
        self.set_press_bool(True)
        widget.get_parent().queue_draw()
        
    def set_press_bool(self, type_bool):
        self.press_bool = type_bool
        
        
    def draw_button(self, widget, event):    
        cr = widget.window.cairo_create()
        x, y, w, h = widget.allocation
                
        draw_background(cr, x, y, w, h, "image/button/button.png")
                    
        if widget.get_child() != None:
            widget.propagate_expose(widget.get_child(), event)
            
        global all_widget    
        
        for w in all_widget:                
            if w.press_bool:
                draw_press_rectangle(cr,
                                     w.allocation.x,
                                     w.allocation.y,
                                     w.allocation.width,
                                     w.allocation.height
                                     )                    
                
        return True
               
class ProgressBar(gtk.Button):
    def __init__(self, max_value=100):
        gtk.Button.__init__(self)
        self.set_size_request(250,25)
        # Init value.
        self.max_value = max_value
        self.press_bool = False
        # Init events.
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)
        
        self.connect("expose-event", self.draw_progressbar)
        self.connect("button-press-event", self.button_press_event)
        
    def button_press_event(self, widget, event):    
        self.set_press_bool(True)
        
    def set_press_bool(self, type_bool):
        self.press_bool = type_bool
        
    def draw_progressbar(self, widget, event):
        cr = widget.window.cairo_create()        
        x, y, w, h = widget.allocation
        
        cr.set_source_rgb(0, 0, 0)
        cr.rectangle(x, y, w, h)
        cr.stroke()
        
        cr.set_source_rgb(0, 0, 1)
        cr.rectangle(x+1, y+1, w/2, h-2)
        cr.fill()
        
        global all_widget    
        
        for w in all_widget:                
            if w.press_bool:
                draw_press_rectangle(cr,
                                     w.allocation.x,
                                     w.allocation.y,
                                     w.allocation.width,
                                     w.allocation.height
                                     )                
    
        return True
    
if __name__ == "__main__":        
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win
    win.show_all()
    gtk.main()
