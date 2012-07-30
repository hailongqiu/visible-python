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

from ini   import Config
from regex import Scan

class CodeEdit(gtk.ScrolledWindow):
    def __init__(self):
        gtk.ScrolledWindow.__init__(self)         
        self.init_code_line_value()
        self.init_row_border()
        self.init_code_folding()
        self.init_border_row_number()
        self.init_cursor()
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
        gtk.timeout_add(888, self.show_and_hide_cursor)
        
    def show_and_hide_cursor(self):    
        if self.cursor_time_bool:
            self.cursor_show_bool = not self.cursor_show_bool
            self.row_ch_queue_draw_area("|")
            
        return self.cursor_time_bool
    
    ###########################################################    
    ### Init value and connect.
    def init_code_line_value(self):    
        self.code_line_padding_x = 888
        self.code_line_color = "#000000"
        self.code_line_alpha = 0.1

    def init_row_border(self):    
        self.row_border_color = "#F5F5F5"
        self.row_border_width = 45
        
    def init_code_folding(self):    
        self.code_folding_width  = 15
        self.code_folding_height = 0
        self.code_folding_bg_alpha   = 1
        self.code_folding_bg_color   = "#FFFFFF"
        self.code_folding_line_alpha = 0.4
        self.code_folding_line_color = "#000000"   
        
    def init_border_row_number(self):    
        self.row_number_color = "#4169E1"
        self.row_number_alpha = 0.8
        self.row_number_padding_x = 15
        
    def init_cursor(self):    
        self.cursor_column = 0
        self.cursor_color = "#000000"
        self.cursor_show_bool = True
        self.cursor_width = 1
        self.cursor_padding_x = 0
        self.cursor_time_bool = False
        
    def init_text_buffer_value(self):    
        self.text_buffer_list = [""]
        self.tab_string = "    "
        self.current_row = 1
        self.cursor_row  = 1        
        self.map_buffer = None
        self.ch_bg_alpha = 0.5
        self.text_source_view_bg_color = "#FFFFFF"
        self.ch_bg_color = "#000000"
        self.scan_file_ini = "language/python.ini"
        
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
        text_utf_8 = text.decode('utf-8')
        for ch in text_utf_8:
            start_string, end_string = self.start_to_end_string(
                self.cursor_row,
                0,
                self.cursor_column,
                self.cursor_column,
                len(self.text_buffer_list[self.cursor_row-1]) + 1
                )
            temp_string = start_string + ch + end_string
            self.text_buffer_list[self.cursor_row - 1] = temp_string
            self.cursor_padding_x += self.get_ch_size(ch)[0]
            self.cursor_column += 1            
            
        self.row_line_queue_draw_area()
        
    def init_text_source_view(self):    
        self.text_source_view = gtk.Button()
        self.text_source_view.set_can_focus(True)
        self.text_source_view.grab_focus()        
        '''Init text_source_view event.'''
        self.text_source_view.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.text_source_view.connect("expose-event",          
                                      self.text_source_view_expose_event)
        self.text_source_view.connect("button-press-event",    
                                      self.text_source_view_button_press_event)
        self.text_source_view.connect("button-release-event",  
                                      self.text_source_view_button_release_event)
        self.text_source_view.connect("key-press-event",       
                                      self.text_source_view_key_press_event)        
        self.text_source_view.connect("focus-out-event",       
                                      self.text_source_view_get_text_view_focus_out)
        self.text_source_view.connect("focus-in-event",        
                                      self.text_source_view_get_text_view_focus_in)
        self.text_source_view.connect("motion-notify-event", 
                                      self.text_source_view_motion_notify_event)
        
    def init_scroll_window_connect(self):    
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.get_hadjustment().connect("value-changed", 
                                       self.scrolled_window_hadjustment_value_changed)
        self.get_vadjustment().connect("value-changed", 
                                       self.scrolled_window_vadjustment_value_changed)
        
    def init_keymap(self):    
        self.keymap = {
            "BackSpace":self.key_delete_ch,
            "Return":self.key_enter,
            "Ctrl + l":self.key_enter_ctrl_l,
            "F11":self.key_full_window
            }
        
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
        self.draw_text_source_view_cursor(cr, rect) 
        # Draw border.
        self.draw_text_source_view_border(widget, cr, rect)
        return True    
    ###
    # expose function.
    ###
    # draw_text_source_view_background.
    def draw_text_source_view_background(self, cr, rect):
        start_index = self.get_scrolled_window_height()[0]
        panent_rect = self.allocation
        self.draw_rectangle(
            cr,
            rect.x,
            rect.y + (start_index * self.row_font_height),
            rect.width,
            # rect.height,
            panent_rect.height,
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
    def draw_text_source_view_buffer_text(self, cr, rect): # 123456
        start_row, end_row, sum_row = self.get_scrolled_window_height()
        start_column, end_column, sum_column = self.get_scrolled_window_width()
        temp_row = 0
        for text in self.get_buffer_row_start_to_end_text(start_row, sum_row):
            all_ch_width = 0
            # get token color.
            if text:
                temp_token_fg_color = {}
                scan = Scan(self.scan_file_ini)
                for table_color in scan.scan(text,  #self.get_buffer_column_start_to_end_text(text, start_column, sum_column)
                                   start_row + temp_row):
                    for column in range(table_color.start_index, 
                                        table_color.end_index+1):
                        temp_token_fg_color[column] = table_color.rgb                        
            temp_token_color_column = 0    
                
            for ch in self.get_buffer_column_start_to_end_text(text, start_column, sum_column):
                temp_ch_width = self.get_ch_size(ch)[0]
                if all_ch_width == None:
                    bg_rgb = "#FF0000"
                else:    
                    bg_rgb = None           
                    
                try:    
                    fg_rgb = temp_token_fg_color[temp_token_color_column]
                except:    
                    fg_rgb = "#000000"
                
                # draw ch.
                x_padding = rect.x + self.get_hadjustment().get_value() + self.row_border_width + self.code_folding_width
                y_padding = rect.y + (start_row + temp_row) * self.row_font_height
                self.draw_text_source_view_buffer_text_ch(
                    ch,
                    cr, 
                    x_padding + all_ch_width,
                    y_padding,
                    fg_rgb,
                    bg_rgb
                    )
                # save ch width.
                all_ch_width += temp_ch_width
                
                temp_token_color_column += 1
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
        #Draw row number.
        self.draw_text_source_view_row_number(cr, rect, -offset_x)

        
    def draw_text_source_view_code_folding(self, cr, rect, offset_x):
        code_folding_x = rect.x + self.row_border_width
        # draw text source code folding background.
        self.draw_alpha_rectangle(
            cr,
            offset_x +  code_folding_x,
            rect.y,
            self.code_folding_width,
            rect.y + rect.height,
            self.code_folding_bg_color,
            self.code_folding_bg_alpha
            )                
        # draw code folding line.
        self.code_folding_height = self.current_row * self.row_font_height
        self.draw_alpha_rectangle(
            cr,
            offset_x + code_folding_x + int(self.code_folding_width/2),
            rect.y,
            1,
            rect.y + self.code_folding_height,
            self.code_folding_line_color,
            self.code_folding_line_alpha
            )        
        
    def draw_text_source_view_row_number(self, cr, rect, offset_x): 
        cr.set_source_rgba(*self.color_to_rgba(self.row_number_color, self.row_number_alpha))
        start_position_row, end_position_row, temp_row = self.get_scrolled_window_height()
                
        if temp_row > self.current_row:
            temp_row = self.current_row
                            
        if self.current_row == 1:
            start_position_row = 0
            temp_row = 1
            
        for row_number in range(start_position_row+1, temp_row+1):
            self.text_buffer_list[row_number - 1] = self.text_buffer_list[row_number-1].replace("\t", self.tab_string)
            context = pangocairo.CairoContext(cr)
            layout = context.create_layout()
            
            temp_font_size = self.font_size
            if row_number == self.cursor_row:
                temp_font_size += 1
            layout.set_font_description(pango.FontDescription("%s %s" % (self.font_type, temp_font_size)))
            (text_width, text_height) = layout.get_pixel_size()            
            
            x_padding = rect.x + offset_x + self.border_width + self.code_folding_width + self.row_number_padding_x
            y_padding = rect.y + (row_number - 1) * self.row_font_height
            layout.set_text(self.row_number_to_string(row_number))
            cr.move_to(
                x_padding,
                y_padding
                )
            context.update_layout(layout)
            context.show_layout(layout)
        
    # draw_text_source_view_cursor.
    def draw_text_source_view_cursor(self, cr, rect):
        if self.cursor_show_bool:
            x_padding = rect.x + self.row_border_width + self.code_folding_width + self.cursor_padding_x
            y_padding = rect.y + (self.cursor_row - 1) * self.row_font_height
            self.draw_rectangle(
                cr,
                x_padding,
                y_padding,
                self.cursor_width,
                self.row_font_height,
                self.cursor_color
                )

    #############################################
    def text_source_view_button_press_event(self, widget, event):
        move_row = int(event.y / self.row_font_height) + 1
        min_row = self.get_scrolled_window_height()[0]
        max_row = self.get_scrolled_window_height()[2]
                                
        if min_row < move_row <= max_row:
            if 1 <= move_row <= self.current_row:
                token_all_width = self.get_press_cursor_position(widget, event, move_row - 1)
                self.cursor_row = move_row            
                self.cursor_padding_x = token_all_width
                self.cursor_show_bool = True
                self.scrolled_window_queue_draw_area()        
                
    def text_source_view_button_release_event(self, widget, event):
        pass
    
    # text_source_view_key_press_event.
    def text_source_view_key_press_event(self, widget, event):
        self.handle_key_press(widget, event)
        
    def handle_key_press(self, widget, event):
        input_method_filt = self.im.filter_keypress(event)
        if not input_method_filt:    
            self.handle_key_event(event)            
        return False        
    
    def handle_key_event(self, event):
        key_name = self.get_keyevent_name(event)        
        print "key_name:" , key_name
        if self.keymap.has_key(key_name):
            self.keymap[key_name]()
    
    # text_source_view_get_text_view_focus_out.        
    def text_source_view_get_text_view_focus_out(self, widget, event):
        self.im.focus_out()        
    
    def text_source_view_get_text_view_focus_in(self, widget, event):
        self.im.set_client_window(widget.window)        
        self.im.focus_in()       
    
    # text_source_view_motion_notify_event.    
    def text_source_view_motion_notify_event(self, widget, event):
        pass
    ############################################################
    '''key map'''
    ###
    def key_delete_ch(self):
        if self.cursor_column > 0:
            start_string, end_string = self.start_to_end_string(
                self.cursor_row,
                0,
                self.cursor_column - 1,
                self.cursor_column,
                len(self.text_buffer_list[self.cursor_row - 1]) + 1
                )
            temp_text = start_string + end_string
            self.text_buffer_list[self.cursor_row - 1] = temp_text 
            
            self.cursor_column = max(self.cursor_column - 1, 0)
        
            if self.cursor_column > 0:
                self.cursor_padding_x = self.get_ch_size(self.text_buffer_list[self.cursor_row - 1][:self.cursor_column])[0]
            else:    
                self.cursor_padding_x = 0                                    
                
            self.row_line_queue_draw_area()    
        else: # if column == 0
            if self.cursor_row > 1:
                temp_text = self.text_buffer_list[self.cursor_row - 1]
                # get cursor position.
                token_all_width = self.get_ch_size(self.text_buffer_list[self.cursor_row - 2])[0]
                # set cursor_column.
                self.cursor_column = len(self.text_buffer_list[self.cursor_row - 2])
                # text_buffer_list connect temp_text.
                self.text_buffer_list[self.cursor_row - 2] += temp_text
                # delete current row text_buffer_list.
                del self.text_buffer_list[self.cursor_row - 1]                
                self.current_row -= 1                
                self.cursor_row  -= 1                
                # set cursor position.
                self.cursor_padding_x = token_all_width
                self.scrolled_window_queue_draw_area()
                
    def key_enter(self):
        temp_text_buffer = self.text_buffer_list[self.cursor_row - 1][:self.cursor_column]        
        temp_insert_text = self.text_buffer_list[self.cursor_row - 1][self.cursor_column:] 
        self.text_buffer_list[self.cursor_row - 1] = temp_text_buffer
        self.text_buffer_list.insert(self.cursor_row, temp_insert_text)        
        self.key_enter_init()
        
    def key_enter_ctrl_l(self):    
        '''Emacs key catl + l'''
        self.text_buffer_list.insert(self.cursor_row, "")
        self.key_enter_init()
        
    def key_enter_init(self):
        self.cursor_padding_x = 0
        self.cursor_column = 0
        self.cursor_row += 1
        self.current_row += 1
        self.scrolled_window_queue_draw_area()

    def key_full_window(self):        
        if self.get_toplevel().window.get_state() == gtk.gdk.WINDOW_STATE_FULLSCREEN:
            self.get_toplevel().unfullscreen()
        else:    
            self.get_toplevel().fullscreen()
            
        
    ############################################################
    '''Operation buffer text.'''    
    ###        
    def read(self, file_path):
        if os.path.exists(file_path):
            self.read_file(file_path)
        else:
            self.perror_input("Read File Error!!......")
            self.text_buffer_list = [""]
            self.current_row = 1
            
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
        self.current_row = sum_row - 1
        
        self.row_border_width += self.get_ch_size(str(self.current_row))[0]
            
    ############################################################    
    '''Tool function.'''
    ###
    def perror_input(self, text):
        print text
        
    def get_buffer_row_start_to_end_text(self, start, end):
        return self.text_buffer_list[start:end]
    
    def get_buffer_column_start_to_end_text(self, text, start, end):
        return text[start:end]
    
    def color_to_rgb(self, color):
        if color[0] == '#': 
            try:
                gdk_color = gtk.gdk.color_parse(color)
                r = (gdk_color.red   / 65535.0)
                g = (gdk_color.green / 65535.0)
                b = (gdk_color.blue  / 65535.0)
                return (r, g, b)
            except Exception, e:
                self.perror_input("color_to_..[Error]:color %s error-->%s"%(color, e))
                return (0, 0, 0)
        else:    
            self.perror_input("color_to_..:color %s '#'"%(color))
            return (0, 0, 0)
            
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
        return (0, 0)
    
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
            
    def row_line_queue_draw_area(self):    
        rect = self.allocation
        self.text_source_view.queue_draw_area(
            rect.x,
            rect.y + (self.cursor_row - 1) * self.row_font_height,
            rect.width,
            self.row_font_height
            )
    def row_ch_queue_draw_area(self, ch):    
        rect = self.allocation
        x_padding = rect.x + self.row_border_width + self.code_folding_width +  self.cursor_padding_x
        y_padding = rect.y + (self.cursor_row - 1) * self.row_font_height
        self.text_source_view.queue_draw_area(
            x_padding,
            y_padding,
            self.get_ch_size(ch)[0],
            self.row_font_height
            )

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
        
    def row_number_to_string(self, row):
        start_len = len(list(str(self.current_row)))
        end_len  = len(list(str(row)))
        num_len = start_len - end_len
        string_row = ""
        for i in xrange(1, num_len+1):
            string_row += "0"
        string_row += str(row)
        return string_row
        
    def get_press_cursor_position(self, widget, event, row):
        '''Get index at event.'''
        rect = widget.allocation
        cr = widget.window.cairo_create()
        context = pangocairo.CairoContext(cr)
        layout = context.create_layout()
        layout.set_font_description(pango.FontDescription("%s %s" % (self.font_size, self.font_size)))
        
        token_all_width = 0
        rect = widget.allocation 
        temp_padding_x =  self.row_border_width + self.code_folding_width
        
        self.cursor_column = 0
        if event.x < temp_padding_x: 
            return 0                
        
        for ch in self.text_buffer_list[row]:
            min_padding_x = (rect.x +  temp_padding_x + token_all_width)
            max_padding_x = (rect.x + temp_padding_x + token_all_width + self.get_ch_size(ch)[0])
            if min_padding_x <= (event.x) <= max_padding_x:
                break
            else:
                self.cursor_column += 1
                token_all_width += self.get_ch_size(ch)[0]
                
        return token_all_width
    
    def get_key_name(self, keyval):    
        key_unicode = gtk.gdk.keyval_to_unicode(keyval)
        
        if key_unicode == 0:
            return gtk.gdk.keyval_name(keyval)
        else:
            return str(unichr(key_unicode))
            
        
    def get_key_event_modifiers(self, key_event): 
        modifiers = [] 
        if key_event.state & gtk.gdk.CONTROL_MASK:
            modifiers.append("Ctrl")            
            
        if key_event.state & gtk.gdk.MOD1_MASK:
            modifiers.append("Alt")
            
        if key_event.state & gtk.gdk.SHIFT_MASK and (len(self.get_key_name(key_event.keyval)) != 1 or not gtk.gdk.keyval_is_upper(key_event.keyval)):        

            modifiers.append("Shift")
    
        return modifiers
    
    def get_keyevent_name(self, key_event):
        if key_event.is_modifier:
            return ""
        else:
            key_modifiers = self.get_key_event_modifiers(key_event)
            key_name      = self.get_key_name(key_event.keyval)
            if key_modifiers == []:
                return key_name
            else:
                if key_name == " ":
                    key_name = "Space"
                return " + ".join(key_modifiers) + " + " + key_name
    
    def start_to_end_string(self, 
                            row, 
                            start_column_1, end_column_1, 
                            start_column_2, end_column_2
                            ):
        start_string = self.text_buffer_list[row - 1][start_column_1:end_column_1]
        end_string   = self.text_buffer_list[row - 1][start_column_2:]
        return start_string, end_string
            
##########################################        
### Test.    
if __name__ == "__main__":
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.set_title("visual python-代码编辑器")
    win.set_size_request(500, 500)
    win.connect("destroy", gtk.main_quit)
    code_edit = CodeEdit()
    code_edit.read("/home/long/123.cpp")
    # code_edit.read("/home/long/123.py")
    win.add(code_edit)
    win.show_all()
    gtk.main()
    
