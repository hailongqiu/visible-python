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
import pango
import pangocairo
from widget import Button, ProgressBar
from tool import draw_press_rectangle, all_widget



class TitleBar(gtk.Fixed):
    def __init__(self):
        gtk.Fixed.__init__(self)
        # init value.
        self.close_bool = True
        self.min_bool   = True
        self.max_bool   = True
        self.text       = "Form"
        self.font_type = "文泉驿微米黑"
        # init pixbuf value.
        self.logo_pixbuf  =  "image/titlebar/logo.ico"
        self.close_pixbuf =  "image/titlebar/window_close_hover.png"
        self.min_pixbuf   =  "image/titlebar/window_min_hover.png"
        self.max_pixbuf   =  "image/titlebar/window_max_hover.png"
        self.icon_width = 25
        self.icon_height = 25
        # init event.
        self.connect("expose-event", self.draw_background)
        
    def size(self, w, h):    
        self.set_size_request(int(w), int(h))
        
    def draw_background(self, widget, event):
        cr = widget.window.cairo_create()
        x, y, w, h = widget.allocation
        cr.set_source_rgb(0, 0, 1)
        cr.rectangle(x, y, w, h)
        cr.fill()
        icon_y = 22
        icon_padding_y = 5
        icon_padding_w = 8
        if self.min_bool:
            self.draw_icon(cr, 
                           self.min_pixbuf,  
                           w-self.icon_width*2 - icon_padding_w, 
                           icon_y)
        if self.max_bool:
            self.draw_icon(cr, 
                           self.max_pixbuf,  
                           w-self.icon_width*1 - icon_padding_w, 
                           icon_y)    
        if self.close_bool:
            self.draw_icon(cr, 
                           self.close_pixbuf, 
                           w-self.icon_width*0 - icon_padding_w, 
                           icon_y)
        icon_x = 22     
        self.draw_logo(cr, 
                       self.logo_pixbuf, 
                       icon_x, 
                       icon_y + icon_padding_y)    
        self.draw_text(cr, 
                       self.text, 
                       x, y, w, h)    
        
        # return True
    
    def draw_logo(self, cr, logo_path, x, y):
        close_pixbuf      = gtk.gdk.pixbuf_new_from_file(logo_path)
        close_scale_pixbf = close_pixbuf.scale_simple(18, 18, gtk.gdk.INTERP_BILINEAR)        
        cr.set_source_pixbuf(close_scale_pixbf, x, y)
        cr.paint_with_alpha(1)

        
    def draw_text(self, cr, text, x, y, w, h):
        font_size = 10
        text_x = 45
        text_y = 26
        context = pangocairo.CairoContext(cr)    
        
        layout = context.create_layout()
        layout.set_font_description(pango.FontDescription("%s %s" % (self.font_type, font_size)))        
        (text_width, text_height) = layout.get_pixel_size()            
        
        layout.set_text(text)
        cr.move_to(text_x, text_y)
        cr.set_source_rgb(1, 1, 1)
        context.update_layout(layout)
        context.show_layout(layout)


    def draw_icon(self, cr, icon_path, x, y):
        close_pixbuf  = gtk.gdk.pixbuf_new_from_file(icon_path)
        close_scale_pixbf = close_pixbuf.scale_simple(self.icon_width, self.icon_height, gtk.gdk.INTERP_BILINEAR)        
        cr.set_source_pixbuf(close_scale_pixbf, x, y)
        cr.paint_with_alpha(1)

#############
# Form 123456
#############
class Form(gtk.EventBox):
    def __init__(self):
        gtk.EventBox.__init__(self)
        # init value.
        self.press_bool = True
        global all_widget
        # Set Form window.
        self.set_visible_window(False)
        
        self.fixed_scroll_ali = gtk.Alignment()
        self.fixed_scroll_ali.set_padding(2, 2, 2, 2)
        self.fixed_scroll = gtk.ScrolledWindow()
        self.fixed_scroll_ali.add(self.fixed_scroll)
        self.fixed_scroll.set_policy(
            # gtk.POLICY_NEVER,            
            # gtk.POLICY_NEVER
            gtk.POLICY_ALWAYS,
            gtk.POLICY_ALWAYS            
            )

        self.fixed = gtk.Fixed()
        self.fixed_scroll.add_with_viewport(self.fixed)
        
        self.add(self.fixed_scroll_ali)
        
        self.text   = "Form"        
        
        self.motion_bool = False
        # Init events.
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.connect("expose-event", self.draw_form_background)
        self.connect("button-press-event", self.set_all_widget_button_press)
        self.fixed.connect("expose-event", self.draw_fixed_background)
        
    def draw_fixed_background(self, widget, event):    
        cr = widget.window.cairo_create()
        x, y, w, h = widget.allocation
        
        cr.set_source_rgb(1, 1, 1)
        cr.rectangle(x, y, w, h)
        cr.fill()

        # # Draw point.
        for x_padding in range(0, w, 5):
            for y_pdding in range(0, h, 5):
                cr.set_source_rgb(0, 0, 0)
                cr.rectangle(x + x_padding, 
                             y + y_pdding, 
                             1, 1)
                cr.fill()
        #         self.draw_rectangle(cr, x + x_padding, y + y_pdding, 0.2, 0.2)

        for w in all_widget:                
            if w.press_bool:
                draw_press_rectangle(cr,
                                     w.allocation.x,
                                     w.allocation.y,
                                     w.allocation.width,
                                     w.allocation.height
                                     )                
                
                self.queue_draw_area(w.allocation.x,
                                     w.allocation.y,
                                     w.allocation.width,
                                     w.allocation.height)
                
    
    def set_all_widget_button_press(self, widget, event):    
        # for w in all_widget:            
        #     w.press_bool = False
            
        # self.press_bool = True
        # self.queue_draw()    
        pass
        # self.get_parent().queue_draw()
        
        
    def put(self, widget, x, y):
        self.fixed.put(widget, x, y)
        all_widget.append(widget)
                
    def size(self, width, height):
        self.set_size_request(int(width), int(height))
        self.fixed_scroll.set_size_request(int(width), int(height))
        
    def draw_form_background(self, widget, event):        
        cr = widget.window.cairo_create()
        x, y, w, h = widget.allocation
        self.draw_background(cr, x, y, w, h)
        
        if self.press_bool:
            # 画虚线方框.
            y_padding = 33
            x_padding = 4        
            w_padding = 6
            h_padding = 35
            self.draw_dash_rectangle(cr, 
                                     x - x_padding, 
                                     y - y_padding, 
                                     w + w_padding, 
                                     h + h_padding)
            ###############################################
            x_padding = 3
            y_padding = 3
            cr.set_dash([],1)
            self.draw_left_rectangle(cr,  
                                     x + x_padding,
                                     y, w, h)
            self.draw_bottom_rectangle(cr, 
                                       x, y + y_padding, w, h)
            self.draw_rangl_rectangle(cr, 
                                      x + x_padding,
                                      y + y_padding, w, h)
        
            
        if "get_child" in dir(widget) and widget.get_child() != None:
            widget.propagate_expose(widget.get_child(), event)
            
        # return True
        
        
    def draw_dash_rectangle(self, cr, x, y, w, h):
        cr.set_source_rgb(0, 0, 0)
        cr.set_dash([1], 0)
        cr.rectangle(x, y, w+2, h+2)
        cr.stroke()
        
    def draw_rectangle(self, cr, x, y, w, h):
        cr.set_source_rgb(1, 1, 1)
        cr.rectangle(x, y, w, h)
        cr.fill()
        
        cr.set_source_rgb(0, 0, 0)
        cr.rectangle(x, y, w, h)
        cr.stroke()
        

    def draw_bottom_rectangle(self, cr, x, y, w, h):    
        padding_w = 7
        padding_h = 7
        self.draw_rectangle(cr, 
                            x + (w / 2 - padding_w/2), 
                            y + (h - padding_h/2),
                            padding_w, padding_h)
    
    def draw_left_rectangle(self, cr, x, y, w, h):
        padding_w = 7
        padding_h = 7
        self.draw_rectangle(cr,
                            x + (w - padding_w/2),
                            y + (h / 2 - padding_h/2),
                            padding_w, padding_h)
        
    def draw_rangl_rectangle(self, cr, x, y, w, h):
        padding_w = 7
        padding_h = 7
        self.draw_rectangle(cr,
                            x + (w - padding_w/2),
                            y + (h - padding_h/2),
                            padding_w, padding_h)
    
    def draw_background(self, cr, x, y, w , h):
        # Draw backround.
        cr.set_source_rgb(1, 1, 1)
        cr.rectangle(x, y, w, h)
        cr.fill()
        
        cr.set_source_rgb(0, 0, 1)
        cr.rectangle(x+1, y+1, w-2, h-2)
        cr.stroke()

        cr.set_source_rgb(0, 0, 1)
        cr.rectangle(x, y, w, h)
        cr.stroke()
        
        # Draw point.
        for x_padding in range(5, w - 3, 5):
            for y_pdding in range(5, h - 3, 5):
                cr.set_source_rgb(0, 0, 0)
                cr.rectangle(x + x_padding, 
                             y + y_pdding, 
                             1, 1)
                cr.fill()
                

################        
# Window class. 123456               
################        
class Window(gtk.Window):
    def __init__(self, window_type=gtk.WINDOW_TOPLEVEL):
        gtk.Window.__init__(self, window_type)
                
        # Init value.
        self.form_x = 20
        self.form_y = 20
        self.form_w = 200
        self.form_h = 200
        self.titlebar_h = 30
        # Init set window.
        self.set_icon_from_file("image/titlebar/logo.ico")
        self.set_title("  visible python  ")        
        self.set_size_request(700, 500)
        
        self.main_fixed = gtk.Fixed()
        self.scroll_form_fixed = gtk.ScrolledWindow()        
        self.event_form_fixed = gtk.EventBox()
        self.event_form_fixed.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.form_fixed       = gtk.Fixed()        
        
        self.event_form_fixed.add(self.form_fixed)
        self.scroll_form_fixed.add_with_viewport(self.event_form_fixed)
        
        self.form_fixed_x = 0
        self.form_fixed_y = 0
        self.form_press_bool = False
        # Init form_fixed events.
        self.form_fixed.connect("expose-event", self.draw_widgets)
        self.event_form_fixed.connect("motion-notify-event", self.motion_modify_mouse_style)
        self.event_form_fixed.connect("button-press-event",   self.drag_press_form_window)
        self.event_form_fixed.connect("button-release-event", self.drag_release_form_window)
        # Init titlbar window.
        self.title_bar = TitleBar()
        self.title_bar.set_size_request(self.form_w + 2, self.titlebar_h)
        # Init form window.        
        self.form = Form()                        
        
        self.button = Button()
        self.button1 = Button()
        
        self.form.put(self.button, 30, 120)
        self.form.put(self.button1, 80, 120)
        
                
        self.form.size(self.form_w, self.form_h)
        
        self.scroll_form_fixed.set_size_request(700, 500)
        self.event_form_fixed.set_size_request(self.form_w, 
                                               self.form_h)
        
        self.form_fixed.put(self.title_bar,
                            self.form_x-1, 
                            self.form_y)
        self.form_fixed.put(self.form, 
                            self.form_x, 
                            self.form_y + self.titlebar_h)
        
        self.main_fixed.put(self.scroll_form_fixed, 100, 100)
        
        self.add(self.main_fixed)
        
    ####################################################    
    # modify mouse icon        
    def motion_modify_mouse_style(self, widget, event):    
        self.modify_mouse_style_function(widget, event)    
        
        if self.form_press_bool:
            mouse_cursot_type = widget.window.get_cursor()
            mouse_state = mouse_cursot_type.get_cursor_type() 
            
            if mouse_state == gtk.gdk.RIGHT_SIDE:
                if event.x > self.form_fixed_x:           
                    form_size_width = self.form.allocation.width   + abs(event.x - self.form_fixed_x)
                else:
                    form_size_width = self.form.allocation.width   - abs(event.x - self.form_fixed_x)
                form_size_height = self.form.allocation.height
            elif mouse_state == gtk.gdk.BOTTOM_SIDE:
                if event.y > self.form_fixed_y:
                    form_size_height = self.form.allocation.height + abs(event.y - self.form_fixed_y)
                    form_size_width = self.form.allocation.width
                else:    
                    form_size_height = self.form.allocation.height - abs(event.y - self.form_fixed_y)
                    form_size_width = self.form.allocation.width
            elif mouse_state == gtk.gdk.BOTTOM_RIGHT_CORNER:
                if event.x > self.form_fixed_x or event.y > self.form_fixed_y:                   
                    form_size_width = self.form.allocation.width   + abs(event.x - self.form_fixed_x)
                    form_size_height = self.form.allocation.height + abs(event.y - self.form_fixed_y)
                else:    
                    form_size_width = self.form.allocation.width   - abs(event.x - self.form_fixed_x)
                    form_size_height = self.form.allocation.height - abs(event.y - self.form_fixed_y)
                
            if form_size_width < 150:        
               form_size_width = 150 
               
            if form_size_height < 100:   
                form_size_height =100
                
            self.form_fixed_x = event.x
            self.form_fixed_y = event.y
            self.form.size(form_size_width,
                           form_size_height)
            self.title_bar.size(form_size_width + 2,
                                30)            
            event_form_fixed_padding = 40
            title_bar_height = 50
            self.event_form_fixed.set_size_request(int(form_size_width) + event_form_fixed_padding, 
                                                   int(form_size_height) + event_form_fixed_padding + title_bar_height)
            # self.queue_draw()
    
    def modify_mouse_style_function(self, widget, event):
        form_x, form_y, form_w, form_h = self.form.allocation
        form_padding= 2
        form_bottom_padding = form_left_padding = 8        
        form_pdding_x = 5
        
        if (form_w + 25 <= event.x <= form_w + form_padding + 30) and (form_h  + 55<= event.y <= form_h + 60): 
            drag = gtk.gdk.BOTTOM_RIGHT_CORNER
            widget.window.set_cursor(gtk.gdk.Cursor(drag))
        elif (form_w - form_pdding_x + 30 <= event.x <= form_w + form_pdding_x + 25) and (form_h/2 - form_left_padding + 45 <= event.y <= form_h/2 + form_left_padding + 45): # left.
            drag = gtk.gdk.RIGHT_SIDE            
            widget.window.set_cursor(gtk.gdk.Cursor(drag))
        elif (form_w/2 - form_bottom_padding  + 10 <= event.x <= form_w/2 + form_bottom_padding + 15) and (form_h + 55  <= event.y <= form_h + 60):    # bottom.
            drag = gtk.gdk.BOTTOM_SIDE
            widget.window.set_cursor(gtk.gdk.Cursor(drag))
        else:
            if not self.form_press_bool:
                widget.window.set_cursor(None)

    def drag_press_event_bool(self, widget, event):            
        form_x, form_y, form_w, form_h = self.form.allocation
        form_padding= 2
        form_bottom_padding = form_left_padding = 8        
        form_pdding_x = 5
        
        if (form_w + 25 <= event.x <= form_w + form_padding + 30) and (form_h + 55 <= event.y <= form_h + 60): 
            self.form_press_bool = True
        elif (form_w - form_pdding_x +30 <= event.x <= form_w + form_pdding_x + 25) and (form_h/2 - form_left_padding + 45 <= event.y <= form_h/2 + form_left_padding + 45): # left.
            self.form_press_bool = True
        elif (form_w/2 - form_bottom_padding +10 <= event.x <= form_w/2 + form_bottom_padding + 15) and (form_h + 55<= event.y <= form_h + 60):    # bottom.
            self.form_press_bool = True
        else:
            self.form_press_bool = False            
            
        if self.form_press_bool:
            self.form_fixed_x = event.x
            self.form_fixed_y = event.y        
        
    def drag_press_form_window(self, widget, event):        
        self.drag_press_event_bool(widget, event)
        
    def drag_release_form_window(self, widget, event):    
        self.form_press_bool = False
    
    def draw_widgets(self, widget, event):
        cr = widget.window.cairo_create()
        x, y, w, h = widget.allocation
        r = g = b = 1.0        
        cr.set_source_rgb(r, g, b)
        cr.rectangle(x, y, w, h)
        cr.fill()
            
    
        # if widget.get_child() != None:
        # widget.propagate_expose(widget.get_child(), event)                
        return False
