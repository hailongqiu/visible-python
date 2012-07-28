#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 Hailong, Inc.
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

import os
import gtk
import mmap
import cairo
import pango
import pangocairo

from ini import Config

class CodeEdit(gtk.ScrolledWindow):
    def __init__(self):
        gtk.ScrolledWindow.__init__(self)            
        
        self.init_code_line_value()
        self.init_row_border()
        self.init_text_buffer_value()
        self.init_language_config()  # init language config.
        self.init_code_edit_config() # init code edit config.
        self.init_font()   # init font-> type and size.    
        self.init_immultiontext()    # init immultiontext.
        self.init_text_source_view() # init text source view.
        self.init_scroll_window_connect() 
        self.init_keymap() # init keymap.
        
        # scrolled window add text source view.
        self.add_with_viewport(self.text_source_view)
        
    ###########################################################    
    ### Init value and connect.
    def init_code_line_value(self):    
        self.code_line_padding_x = 888
        self.code_line_color = "#000000"
        self.code_line_alpha = 0.1

    def init_row_border(self):    
        self.row_border_color = "#F5F5F5"
        self.row_border_width = 70
        
    def init_text_buffer_value(self):    
        self.text_buffer_list = []
        self.map_buffer = None
        self.ch_bg_alpha = 0.5
        self.text_source_view_bg_color = "#FFFFFF"
        self.ch_bg_color = "#000000"
        
    def init_language_config(self, config_path="language/python.ini"):
        self.language_config = Config(config_path)
        
    def init_code_edit_config(self, config_path=".config/visual_python/code_edit.ini"):
        self.code_edit_config = Config(config_path)
        
    def init_font(self, font_type="文泉驿等宽微米黑", font_size=11):                    
        '''Init font type/size.'''
        self.font_type  = "文泉驿等宽微米黑"
        self.font_size  = 11
        self.column_font_width = self.get_ch_size(" ")[0]
        self.row_font_height = self.get_ch_size(" ")[1]        
        
    def init_immultiontext(self):
        '''Init immulticontext.'''
        self.im = gtk.IMMulticontext()
        self.im_offset_x = 0
        self.im_offset_y = 0
        self.im.connect("commit", self.get_im_input_string)
        
    def get_im_input_string(self, IMMulticontext, text):    
        print "get_im_input_string:", text
        
    def init_text_source_view(self):    
        self.text_source_view = gtk.Button()
        self.text_source_view.set_can_focus(True)
        self.text_source_view.grab_focus()        
        '''Init text_source_view event.'''
        self.text_source_view.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.text_source_view.connect("expose-event",          self.text_source_view_expose_event)
        self.text_source_view.connect("button-press-event",    self.text_source_view_button_press_event)
        self.text_source_view.connect("button-release-event",  self.text_source_view_button_release_event)
        self.text_source_view.connect("key-press-event",       self.text_source_view_key_press_event)        
        self.text_source_view.connect("focus-out-event",       self.text_source_view_get_text_view_focus_out)
        self.text_source_view.connect("focus-in-event",        self.text_source_view_get_text_view_focus_in)
        self.text_source_view.connect("motion-notify-event",   self.text_source_view_motion_notify_event)
        
    def init_scroll_window_connect(self):    
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.get_hadjustment().connect("value-changed", self.scrolled_window_hadjustment_value_changed)
        self.get_vadjustment().connect("value-changed", self.scrolled_window_vadjustment_value_changed)
        
    def init_keymap(self):    
        self.keymap = {}
        
    ############################################################    
    ### scrolled window connect.
    def scrolled_window_hadjustment_value_changed(self, hadjustment):
        self.scrolled_window_queue_draw_area()
    
    def scrolled_window_vadjustment_value_changed(self, vadjustment):    
        self.scrolled_window_queue_draw_area()
    
    ############################################################
    ### text source view connect.
        
    ###############    
    ''' expose function: background, border, row number, buffer text, hight... ...'''
    ###    
    def text_source_view_expose_event(self, widget, event):
        cr = widget.window.cairo_create() # create cairo.
        rect = widget.allocation # text source view allocation(x, y, width, height)
        
        # Draw background.
        self.draw_text_source_view_background(cr, rect)
        # Draw code line.
        self.draw_text_source_view_code_line(cr, rect)
        # Draw buffer text.
        self.draw_text_source_view_buffer_text(cr, rect)
        # Draw cursor.
        # self.draw_text_source_view_cursor(cr, rect) 
        # Draw border.
        self.draw_text_source_view_border(widget, cr, rect)
        return True
    ###
    # expose function.
    ###
    # draw_text_source_view_background.
    def draw_text_source_view_background(self, cr, rect):
        self.draw_rectangle(
            cr, 
            rect.x, 
            rect.y,
            rect.width,
            rect.height,
            self.text_source_view_bg_color)
        
    # draw_text_source_view_code_line.
    def draw_text_source_view_code_line(self, cr, rect):
        self.draw_alpha_rectangle(
            cr,
            rect.x + self.code_line_padding_x,
            rect.y,
            1,
            rect.y + rect.height,
            self.code_line_color, 
            self.code_line_alpha            
            )
        
    # draw_text_source_view_buffer_text.
    def draw_text_source_view_buffer_text(self, cr, rect):
        start_row, end_row, sum_row = self.get_scrolled_window_height()
        start_column, end_column, sum_column = self.get_scrolled_window_width()
        temp_row = 0
        for text in self.get_buffer_row_start_to_end_text(start_row, sum_row):
            all_ch_width = 0
            for ch in self.get_buffer_column_start_to_end_text(text, start_column, sum_column):
                temp_ch_width = self.get_ch_size(ch)[0]
                if all_ch_width == 0:
                    bg_rgb = "#FF0000"
                else:    
                    bg_rgb = None           
                # draw ch.
                self.draw_text_source_view_buffer_text_ch(
                    ch, 
                    cr, 
                    rect.x + self.get_hadjustment().get_value() + self.row_border_width + all_ch_width, 
                    rect.y + (start_row + temp_row) * self.row_font_height, 
                    self.ch_bg_color,
                    bg_rgb
                    )                
                # save ch width.    
                all_ch_width += temp_ch_width
            temp_row += 1    
            
    def draw_text_source_view_buffer_text_ch(self, ch, cr, 
                                             offset_x, offset_y, 
                                             fg_rgb, bg_rgb=None
                                             ):    
        context = pangocairo.CairoContext(cr)            
        layout = context.create_layout()
        layout.set_font_description(pango.FontDescription("%s %s" % (self.font_type, self.font_size))) 
        ch_width, ch_height = self.get_ch_size(ch)
        # set ch background color.
        self.set_ch_background(
            cr, 
            offset_x, offset_y, 
            ch_width, ch_height, 
            self.ch_bg_alpha, bg_rgb
            )
        # Set font position.
        layout.set_text(ch)
        cr.move_to(offset_x, 
                   offset_y)        
        # Set font rgb.
        cr.set_source_rgb(*self.color_to_rgb(fg_rgb))            
        # Show font.
        context.update_layout(layout)
        context.show_layout(layout)        
                
    def set_ch_background(self, cr, 
                          offset_x, offset_y, 
                          ch_width, ch_height, 
                          alpha, bg_rgb=None
                          ):    
        if bg_rgb:
            self.draw_alpha_rectangle(
                cr,
                offset_x, 
                offset_y, 
                ch_width, 
                ch_height,
                bg_rgb, 
                alpha
                )
            
    # draw_text_source_view_border.        
    def draw_text_source_view_border(self, widget, cr, rect):
        offset_x, offset_y = self.get_coordinates(widget, rect.x, rect.y)
        # Draw border.
        cr.set_source_rgb(*self.color_to_rgb(self.row_border_color))
        cr.rectangle(-offset_x,
                     rect.y,
                     self.row_border_width,
                     rect.height)
        cr.fill()
        # Draw code folding.
        self.draw_text_source_view_code_folding(cr, rect, -offset_x)        

    def draw_text_source_view_code_folding(self, cr, rect, offset_x):
        # self.draw_alpha_rectangle(
        #     cr,
        #     -offset_x +  code_folding_x
        #     )
        # temp_code_folding_x = 3
        # cr.set_source_rgb(*self.color_to_rgb("#FFFFFF"))
        # code_folding_x = rect.x + self.row_border_width 
        # # draw code folding background.
        # cr.rectangle(,
        #               rect.y,
        #               self.text_view_padding_x,
        #               rect.y + rect.height)
        # cr.fill()        
        pass
    
    # draw_text_source_view_cursor.
    # def draw_text_source_view_cursor(self, ):    
    
    #############################################    
    def text_source_view_button_press_event(self, widget, event):
        pass
    
    def text_source_view_button_release_event(self, widget, event):
        pass
    
    def text_source_view_key_press_event(self, widget, event):
        pass
    
    def text_source_view_get_text_view_focus_out(self, widget, event):
        self.im.focus_out()        
    
    def text_source_view_get_text_view_focus_in(self, widget, event):
        self.im.set_client_window(widget.window)        
        self.im.focus_in()       
    
    def text_source_view_motion_notify_event(self, widget, event):
        pass        
    
    ############################################################
    '''Operation buffer text.'''    
    ###
    def read(self, file_path):
        if os.path.exists(file_path):
            self.read_file(file_path)
        else:    
            self.perror("讀取文件錯誤!!")
    
    def read_file(self, file_path):
        self.file_path = file_path                                        
        with open(self.file_path, "r") as f:
            self.map_buffer = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        # buffer list.
        temp_text_buffer_list = str(self.map_buffer[:]).decode("utf-8").split("\n")        
        # sum row.
        sum_row = len(temp_text_buffer_list)
        # save max column.
        max_column = 0        
        # get text_buffer_list max colume.
        for row in xrange(0, sum_row-1):
            if len(temp_text_buffer_list[row]) > max_column:
                max_column = len(temp_text_buffer_list[row])
        # set size.
        text_source_view_padding_height = 580
        text_source_view_padding_width  = 580
        self.text_source_view.set_size_request(
            max_column * self.column_font_width + text_source_view_padding_width,
            sum_row * self.row_font_height + text_source_view_padding_height
            ) 
        self.text_buffer_list = temp_text_buffer_list
        
    ############################################################    
    '''Tool function.'''
    ###
    def get_buffer_row_start_to_end_text(self, start, end):
        return self.text_buffer_list[start:end]
    
    def get_buffer_column_start_to_end_text(self, text, start, end):
        return text[start:end]
    
    def color_to_rgb(self, color):
        if color[0] == '#': 
            gdk_color = gtk.gdk.color_parse(color)
            return (gdk_color.red / 65535.0, gdk_color.green / 65535.0, gdk_color.blue / 65535.0)
        
    def color_to_rgba(self, color, alpha):    
        r,g,b = self.color_to_rgb(color)
        return r, g, b, alpha
    
    def get_ch_size(self, ch):    
        if ch:
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 0, 0)
            cr = cairo.Context(surface)
            context = pangocairo.CairoContext(cr)
            layout = context.create_layout()
            layout.set_font_description(pango.FontDescription("%s %s" % (self.font_type, self.font_size)))
            layout.set_text(ch)
            return layout.get_pixel_size()
        
    def get_scrolled_window_height(self):
        '''Get row of scrolled window current height.'''
        start_position_row = int(self.get_vadjustment().get_value() / self.row_font_height)
        end_position_row   = int(self.allocation.height / self.row_font_height)
        start_to_end_row   = end_position_row + start_position_row
        return start_position_row, end_position_row, start_to_end_row
    
    def get_scrolled_window_width(self):
        '''Get column of scrolled window current width.'''
        start_position_column = int(self.get_hadjustment().get_value() / self.column_font_width)
        end_position_column   = int(self.allocation.width / self.column_font_width)
        start_to_end_column   = start_position_column + end_position_column
        return start_position_column, end_position_column, start_to_end_column
                    
    def scrolled_window_queue_draw_area(self):            
        rect = self.allocation
        self.text_source_view.queue_draw_area(
            rect.x,
            rect.y,
            rect.width,
            rect.height
            )
        self.queue_draw()
    
    def get_coordinates(self, widget, x, y):
        return widget.translate_coordinates(self, x, y)
        
    def draw_rectangle(self, cr, x, y, w, h, rgb):
        cr.set_source_rgb(*self.color_to_rgb(rgb))
        cr.rectangle(x, y, w, h)
        cr.fill()
    
    def draw_alpha_rectangle(self, cr, x, y, w, h, rgb, alpha):
        cr.set_source_rgba(*self.color_to_rgba(rgb, alpha))
        cr.rectangle(x, y, w, h)
        cr.fill()
        
##########################################        
### Test.    
if __name__ == "__main__":
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.set_title("visual python-代码编辑器")
    win.connect("destroy", gtk.main_quit)
    code_edit = CodeEdit()
    code_edit.read("/home/long/123.txt")
    win.add(code_edit)
    win.show_all()
    gtk.main()
    
