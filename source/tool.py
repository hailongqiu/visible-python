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


all_widget = []

def draw_background(cr, x, y, w, h, pixbuf_path):
    button_pixbuf = gtk.gdk.pixbuf_new_from_file(pixbuf_path)
    button_scale_pixbuf = button_pixbuf.scale_simple(w, h, gtk.gdk.INTERP_BILINEAR)        
    cr.set_source_pixbuf(button_scale_pixbuf, x, y)
    cr.paint_with_alpha(1)                                
    
def draw_press_rectangle(cr, x, y, w, h):
    min_rectange_w = min_rectange_h = 5    
    max_rectange_w = w + min_rectange_w
    max_rectange_h = h + min_rectange_h
    x = x - min_rectange_w/2 - 1
    y = y - min_rectange_h/2 - 1
    # dash rectangle.
    cr.set_source_rgb(0, 0, 0)
    cr.set_dash([1], 1)
    cr.rectangle(x , y, max_rectange_w, max_rectange_h)
    cr.stroke()
        
    
    # top left.
    cr.set_source_rgb(1, 1, 1)
    cr.rectangle(x - (min_rectange_w/2), 
                 y - (min_rectange_h/2),
                 min_rectange_w,
                 min_rectange_h)
    cr.fill()
    cr.set_source_rgb(0, 0, 0)
    cr.set_dash([], 1)
    cr.rectangle(x - (min_rectange_w/2), 
                 y - (min_rectange_h/2),
                 min_rectange_w,
                 min_rectange_h)
    cr.stroke()
    # top.    
    cr.set_source_rgb(1, 1, 1)
    cr.rectangle(x + max_rectange_w/2, 
                 y - min_rectange_h/2, 
                 min_rectange_w, 
                 min_rectange_h)
    cr.fill()
    cr.set_source_rgb(0, 0, 0)
    cr.rectangle(x + max_rectange_w/2, 
                 y - min_rectange_h/2, 
                 min_rectange_w, 
                 min_rectange_h)
    cr.stroke()
    # top right.    
    cr.set_source_rgb(1, 1, 1)
    cr.rectangle(x + max_rectange_w - min_rectange_w/2, 
                 y - min_rectange_h/2, 
                 min_rectange_w,
                 min_rectange_h)

    cr.fill()
    cr.set_source_rgb(0, 0, 0)
    cr.rectangle(x + max_rectange_w - min_rectange_w/2, 
                 y - min_rectange_h/2, 
                 min_rectange_w,
                 min_rectange_h)
    cr.stroke()
    # right.    
    cr.set_source_rgb(1, 1, 1)
    cr.rectangle(x + max_rectange_w - min_rectange_w/2, 
                 y + max_rectange_h/2- min_rectange_h/2,
                 min_rectange_w,
                 min_rectange_h)    
    cr.fill()
    cr.set_source_rgb(0, 0, 0)
    cr.rectangle(x + max_rectange_w - min_rectange_w/2, 
                 y + max_rectange_h/2- min_rectange_h/2,
                 min_rectange_w,
                 min_rectange_h)
    cr.stroke()
    # bottom right.    
    cr.set_source_rgb(1, 1, 1)
    cr.rectangle(x + max_rectange_w- min_rectange_w/2, 
                 y + max_rectange_h- min_rectange_h/2, 
                 min_rectange_w,
                 min_rectange_h)    
    cr.fill()
    cr.set_source_rgb(0, 0, 0)    
    cr.rectangle(x + max_rectange_w- min_rectange_w/2, 
                 y + max_rectange_h- min_rectange_h/2, 
                 min_rectange_w,
                 min_rectange_h)
    cr.stroke()
    # bottom.    
    cr.set_source_rgb(1, 1, 1)
    cr.rectangle(x + max_rectange_w/2, 
                 y + max_rectange_h - min_rectange_h/2, 
                 min_rectange_w,
                 min_rectange_h)
    cr.fill()
    cr.set_source_rgb(0, 0, 0)        
    cr.rectangle(x + max_rectange_w/2, 
                 y + max_rectange_h- min_rectange_h/2, 
                 min_rectange_w,
                 min_rectange_h)
    cr.stroke()
    # bottom left.    
    cr.set_source_rgb(1, 1, 1)
    cr.rectangle(x - min_rectange_w/2, 
                 y + max_rectange_h - min_rectange_h/2, 
                 min_rectange_w,
                 min_rectange_h)    
    cr.fill()
    cr.set_source_rgb(0, 0, 0)            
    cr.rectangle(x - min_rectange_w/2, 
                 y + max_rectange_h - min_rectange_h/2, 
                 min_rectange_w,
                 min_rectange_h)
    cr.stroke()
    # left.    
    cr.set_source_rgb(1, 1, 1)
    cr.rectangle(x - min_rectange_w/2, 
                 y + max_rectange_h/2 - min_rectange_h/2, 
                 min_rectange_w,
                 min_rectange_h)    
    cr.fill()
    cr.set_source_rgb(0, 0, 0)                
    cr.rectangle(x - min_rectange_w/2, 
                 y + max_rectange_h/2 - min_rectange_h/2, 
                 min_rectange_w,
                 min_rectange_h)
    cr.stroke()

    
    
def modify_window_mouse_icon(widget, event, x, y, w, h):
    '''GDK_BOTTOM_LEFT_CORNER
       GDK_BOTTOM_RIGHT_CORNER       
       GDK_BOTTOM_SIDE
       GDK_LEFT_SIDE
       GDK_RIGHT_SIDE
       GDK_TOP_LEFT_CORNER
       GDK_TOP_RIGHT_CORNER
       GDK_TOP_SIDE
    '''    
    min_rectange_w = min_rectange_h = 5    
    max_rectange_w = w + min_rectange_w
    max_rectange_h = h + min_rectange_h
    x = x - min_rectange_w/2 - 1
    y = y - min_rectange_h/2 - 1
    if True:
        if (x - (min_rectange_w/2) <= event.x <= x - (min_rectange_w/2) + min_rectange_w) and (y - (min_rectange_h/2)<= event.y <= y - (min_rectange_h/2) + min_rectange_h): ### GDK_TOP_LEFT_CORNER
            drag = gtk.gdk.TOP_LEFT_CORNER
            widget.window.set_cursor(gtk.gdk.Cursor(drag))    
        elif (x + max_rectange_w/2 <= event.x <= x + max_rectange_w/2 + min_rectange_w) and (y - min_rectange_h/2 <= event.y <= y - min_rectange_h/2 + min_rectange_h): ### GDK_TOP_SIDE
            drag = gtk.gdk.TOP_SIDE
            widget.window.set_cursor(gtk.gdk.Cursor(drag))    
        elif (x + max_rectange_w - min_rectange_w/2 <= event.x <= x + max_rectange_w - min_rectange_w/2 + min_rectange_w) and (y - min_rectange_h/2 <= event.y <= y - min_rectange_h/2 + min_rectange_h): ### GDK_TOP_RIGHT_CORNER   
            drag = gtk.gdk.TOP_RIGHT_CORNER
            widget.window.set_cursor(gtk.gdk.Cursor(drag))    
        elif (x + max_rectange_w - min_rectange_w/2 <= event.x <= x + max_rectange_w - min_rectange_w/2 + min_rectange_w) and (y + max_rectange_h/2- min_rectange_h/2 <= event.y <= y + max_rectange_h/2- min_rectange_h/2 + min_rectange_h): ### GDK_RIGHT_SIDE
            drag = gtk.gdk.RIGHT_SIDE
            widget.window.set_cursor(gtk.gdk.Cursor(drag))    
        elif (x + max_rectange_w- min_rectange_w/2 <= event.x <= x + max_rectange_w- min_rectange_w/2 + min_rectange_w) and (y + max_rectange_h- min_rectange_h/2 <= event.y <= y + max_rectange_h- min_rectange_h/2 + min_rectange_h): ### GDK_BOTTOM_RIGHT_CORNER 
            drag = gtk.gdk.BOTTOM_RIGHT_CORNER
            widget.window.set_cursor(gtk.gdk.Cursor(drag))    
        elif (x + max_rectange_w/2 <= event.x <= x + max_rectange_w/2 + min_rectange_w) and (y + max_rectange_h - min_rectange_h/2 <= event.y <= y + max_rectange_h - min_rectange_h/2 + min_rectange_h): ### GDK_BOTTOM_SIDE
            drag = gtk.gdk.BOTTOM_SIDE
            widget.window.set_cursor(gtk.gdk.Cursor(drag))    
        elif (x - min_rectange_w/2 <= event.x <= x - min_rectange_w/2 + min_rectange_w) and (y + max_rectange_h - min_rectange_h/2 <= event.y <= y + max_rectange_h - min_rectange_h/2 + min_rectange_h):
            drag = gtk.gdk.BOTTOM_LEFT_CORNER
            widget.window.set_cursor(gtk.gdk.Cursor(drag))    
        elif (x - min_rectange_w/2 <= event.x <= x - min_rectange_w/2 + min_rectange_w) and (y + max_rectange_h/2 - min_rectange_h/2 <= event.y <= y + max_rectange_h/2 - min_rectange_h/2 + min_rectange_h):    
            drag = gtk.gdk.LEFT_SIDE
            widget.window.set_cursor(gtk.gdk.Cursor(drag))                
        # else:    
        #     widget.window.set_cursor(None)
    

def modify_widget_mouse_icon(widget, event, x, y, w, h):
    '''GDK_BOTTOM_LEFT_CORNER
       GDK_BOTTOM_RIGHT_CORNER       
       GDK_BOTTOM_SIDE
       GDK_LEFT_SIDE
       GDK_RIGHT_SIDE
       GDK_TOP_LEFT_CORNER
       GDK_TOP_RIGHT_CORNER
       GDK_TOP_SIDE
       '''    
    rect = widget.allocation
    
    min_rectange_w = min_rectange_h = 5    
    max_rectange_w = w + min_rectange_w
    max_rectange_h = h + min_rectange_h
    x = x - min_rectange_w/2 - 1
    y = y - min_rectange_h/2 - 1    
        
    if (x - (min_rectange_w/2) <= rect.x + event.x <= x - (min_rectange_w/2) + min_rectange_w):
        print "*************modify widget mouse icon.."
        
    if True:
        if (x - (min_rectange_w/2) <= rect.x + event.x <= x - (min_rectange_w/2) + min_rectange_w) and (y - (min_rectange_h/2)<= rect.y + event.y <= y - (min_rectange_h/2) + min_rectange_h): ### GDK_TOP_LEFT_CORNER
            drag = gtk.gdk.TOP_LEFT_CORNER
            widget.window.set_cursor(gtk.gdk.Cursor(drag))    
        elif (x + max_rectange_w/2 <= rect.x + event.x <= x + max_rectange_w/2 + min_rectange_w) and (y - min_rectange_h/2 <= rect.y + event.y <= y - min_rectange_h/2 + min_rectange_h): ### GDK_TOP_SIDE
            drag = gtk.gdk.TOP_SIDE
            widget.window.set_cursor(gtk.gdk.Cursor(drag))    
        elif (x + max_rectange_w - min_rectange_w/2 <= rect.x + event.x <= x + max_rectange_w - min_rectange_w/2 + min_rectange_w) and (y - min_rectange_h/2 <= rect.y + event.y <= y - min_rectange_h/2 + min_rectange_h): ### GDK_TOP_RIGHT_CORNER   
            drag = gtk.gdk.TOP_RIGHT_CORNER
            widget.window.set_cursor(gtk.gdk.Cursor(drag))    
        elif (x + max_rectange_w - min_rectange_w/2 <= rect.x + event.x <= x + max_rectange_w - min_rectange_w/2 + min_rectange_w) and (y + max_rectange_h/2- min_rectange_h/2 <= rect.y + event.y <= y + max_rectange_h/2- min_rectange_h/2 + min_rectange_h): ### GDK_RIGHT_SIDE
            drag = gtk.gdk.RIGHT_SIDE
            widget.window.set_cursor(gtk.gdk.Cursor(drag))    
        elif (x + max_rectange_w- min_rectange_w/2 <= rect.x + event.x <= x + max_rectange_w- min_rectange_w/2 + min_rectange_w) and (y + max_rectange_h- min_rectange_h/2 <= rect.y + event.y <= y + max_rectange_h- min_rectange_h/2 + min_rectange_h): ### GDK_BOTTOM_RIGHT_CORNER 
            drag = gtk.gdk.BOTTOM_RIGHT_CORNER
            widget.window.set_cursor(gtk.gdk.Cursor(drag))    
        elif (x + max_rectange_w/2 <= rect.x + event.x <= x + max_rectange_w/2 + min_rectange_w) and (y + max_rectange_h - min_rectange_h/2 <= rect.y + event.y <= y + max_rectange_h - min_rectange_h/2 + min_rectange_h): ### GDK_BOTTOM_SIDE
            drag = gtk.gdk.BOTTOM_SIDE
            widget.window.set_cursor(gtk.gdk.Cursor(drag))    
        elif (x - min_rectange_w/2 <= rect.x + event.x <= x - min_rectange_w/2 + min_rectange_w) and (y + max_rectange_h - min_rectange_h/2 <= rect.y + event.y <= y + max_rectange_h - min_rectange_h/2 + min_rectange_h):
            drag = gtk.gdk.BOTTOM_LEFT_CORNER
            widget.window.set_cursor(gtk.gdk.Cursor(drag))    
        elif (x - min_rectange_w/2 <= rect.x + event.x <= x - min_rectange_w/2 + min_rectange_w) and (y + max_rectange_h/2 - min_rectange_h/2 <= rect.y + event.y <= y + max_rectange_h/2 - min_rectange_h/2 + min_rectange_h):    
            drag = gtk.gdk.LEFT_SIDE
            widget.window.set_cursor(gtk.gdk.Cursor(drag))                
        # else:    
        #     widget.window.set_cursor(None)
            
            
def drag_widget_size(widget):
    pass


    
