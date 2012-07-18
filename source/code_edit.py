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
import pangocairo
import pango
import cairo
from collections import OrderedDict
import threading



class CodeEdit(gtk.ScrolledWindow):
    def __init__(self,
                 buffer=None):
        gtk.ScrolledWindow.__init__(self)
        #######################################
        ###
        
        #######################################
        ### init imm.
        '''Init IMMulticontext.'''
        self.im = gtk.IMMulticontext()
        self.im.connect("commit", self.get_im_input_string)
        #######################################
        ### init value.
        '''Init font type/size.'''
        self.font_type  = "文泉驿等宽微米黑"
        self.font_size  = 11
        '''Init value.'''
        self.buffer = []
        self.buffer_dict = OrderedDict
        self.buffer_dict = {}
        self.current_row    = 1
        self.current_colume = 0
        self.row_border_width = 70                
        self.expose_row_border_bool = False
        self.text_view_padding_x = 15
        '''Init Operation.'''
        self.start_index     = 0
        self.end_index       = 0
        self.start_index_padding_x   = 0
        self.end_index_padding_x     = 0        
        self.move_copy_bool  = False
        self.move_copy_color = "#000000"
        self.move_copy_alpha = 0.2
        '''Init code number.'''
        self.code_number_color = "#000000"
        self.code_number_alpha = 0.5
        self.code_number_padding_x = 10
        '''Init color.'''
        self.bg_color                  = "#FFFFFF"
        self.row_border_color          = "#F5F5F5"        
        '''Init text_view_rectangle'''
        self.text_view_rectangle_color = "#7FFFD4"
        self.text_view_rectangle_alpha = 0.2
        '''Init code line.'''
        self.code_line_padding_x = 888
        self.code_line_alpha     = 0.1
        self.code_line_color  = "#000000"        
        '''Init code string.'''
        self.code_font_width  = self.get_ch_size(" ")[0]
        self.code_font_height = self.get_ch_size(" ")[1]        
        '''Init cursor value'''
        self.cursor_color  = "#000000"
        self.cursor_height = self.code_font_height
        self.cursor_padding_x = 0
        self.cursor_row    = 1
        self.cursor_column = 0
        self.cursor_show_bool = True
        self.cursor_time      = 888
        '''Init code folding.'''
        self.code_folding_height = self.code_font_height
        self.code_folding_color  = "#000000"
        self.code_folding_alpha  = 0.4
        '''Init Tab.'''
        self.Tab_BackSpace_Num = 4    # if == 0-> /t > 0 BackSpace.
        '''Init keymap.'''
        self.keymap = {
            "Tab":self.Set_Tab,
            "Ctrl + a":self.Cursor_Row_Start,
            "Ctrl + e":self.Cursor_Row_End,
            "Ctrl + f":self.Cursor_Right,
            "Ctrl + b":self.Cursor_Left,
            "Ctrl + p":self.Cursor_Up,
            "Ctrl + n":self.Cursor_Down,
            "F11":self.full_window,
            "Return":self.Enter,
            "Ctrl + l":self.Smart_Enter,
            "BackSpace":self.Delete_Ch
            }
        ########################################
        ### text_source_view.
        '''Init text_source_view.'''
        self.text_source_view = gtk.Button()
        self.text_source_view.set_size_request(888, 800)
        self.text_source_view.set_can_focus(True)
        self.text_source_view.grab_focus()        
        '''Init text_source_view event.'''
        self.text_source_view.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.text_source_view.connect("expose-event",          self.expose_draw_text_source_view)                
        self.text_source_view.connect("button-press-event",    self.button_press_event)
        self.text_source_view.connect("button-release-event",  self.button_release_event)
        self.text_source_view.connect("key-press-event",       self.key_press_event)        
        self.text_source_view.connect("focus-out-event",       self.get_text_view_focus_out)
        self.text_source_view.connect("focus-in-event",        self.get_text_view_focus_in)
        self.text_source_view.connect("motion-notify-event",   self.motion_notify_event)        
        
        # ScrolledWindow event.
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.get_hadjustment().connect("value-changed", self.scrolled_window_value_changed)
        self.get_vadjustment().connect("value-changed", self.scrolled_window_vadjustment_value_changed)
        ########################################
        ### add text_source_view.
        self.add_with_viewport(self.text_source_view)
        
        gtk.timeout_add(self.cursor_time, self.set_cursor_show_bool_time)
        
    def set_cursor_show_bool_time(self):    
        self.cursor_show_bool = not self.cursor_show_bool
        self.queue_draw()
        return True
    
    def button_release_event(self, widget, event):
        self.move_copy_bool = False
        
    def motion_notify_event(self, widget, event):    
        self.expose_row_border_bool = False
        
        if self.move_copy_bool:
            # Get cursor_padding_x  start index x.
            self.start_index = self.current_colume
            self.start_index_padding_x = self.cursor_padding_x
            self.end_index, self.end_index_padding_x = self.get_motion_cursor_position(widget, event, self.cursor_row)
            self.queue_draw()
            
    def get_motion_cursor_position(self, widget, event, row):
        '''Get index at event.'''
        rect = widget.allocation
        cr = widget.window.cairo_create()
        context = pangocairo.CairoContext(cr)
        layout = context.create_layout()
        layout.set_font_description(pango.FontDescription("%s %s" % (self.font_size, self.font_size)))
        
        token_string = ""
        token_all_width = 0
        rect = widget.allocation
        temp_colume = 0
        
        if ((self.row_border_width + self.text_view_padding_x) < event.x):
            if self.buffer_dict.has_key(row):
                for table in self.buffer_dict[row]:
                    token_string += table.token_ch                
                    temp_padding_x = token_all_width + self.row_border_width + self.text_view_padding_x
                
                    if (rect.x +  temp_padding_x) <=  int(rect.x + event.x) <= (rect.x + temp_padding_x + table.token_width):
                        break
                    else:
                        token_all_width += table.token_width
                        temp_colume += 1
                        
        return temp_colume, token_all_width
    
    
    def scrolled_window_value_changed(self, adjustment):  
        self.expose_row_border_bool = True
        self.text_source_view.queue_draw()
        
    def scrolled_window_vadjustment_value_changed(self, vadjustment):    
        self.expose_row_border_bool = False
        self.text_source_view.queue_draw()
        
    ################################################        
    # Set imm.    
    def get_im_input_string(self, IMMulticontext, text):
        # print "text:", text
        text_utf_8 = text.decode('utf-8')
        
        for ch in text_utf_8:
            table = Table()
            table.token_ch = ch
            table.token_width, table.token_height = self.get_ch_size(ch)
            table.token_row = self.cursor_row
            
            self.set_token_ch_color(ch, table)
            
            if self.buffer_dict.has_key(self.cursor_row):
                self.buffer_dict[self.cursor_row].insert(self.current_colume, table)
            else:
                self.buffer_dict[self.cursor_row] = []
                self.buffer_dict[self.cursor_row].insert(0, table)
                                
            self.cursor_padding_x += self.get_ch_size(ch)[0]
            
            # get current cursor position.  
            self.get_current_cursor_colume()
        
        self.queue_draw()
        
    def set_token_ch_color(self, ch, table):    
        # Test hight.
        
        if ch in ["邱", "海", "龙", "暴", "风"]:
            table.token_rgb = "#F08080"
        elif ch in ["d", "e", "f"]:    
            table.token_rgb = "#5F9EA0"
        elif ch in ["深", "度"]:
            table.token_rgb = "#800000"
        elif ch in ['L', 'i', 'n', 't']:
            table.token_rgb = "#7B68EE"
        elif ch in ['c', 'l', 'a', 's']:    
            table.token_rgb = "#008000"
        
    def get_current_row_string_bool(self):    
        for table in self.buffer:
            if table.token_row == self.cursor_row:
                return True         
        return False    
            
    def get_current_cursor_colume(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 0, 0)
        cr = cairo.Context(surface)
        context = pangocairo.CairoContext(cr)
        layout = context.create_layout()
        layout.set_font_description(pango.FontDescription("%s %s" % (self.font_size, self.font_size)))

        self.current_colume = 0
        token_string = ""
        token_all_width = 0
        
        if self.buffer_dict.has_key(self.cursor_row):
            for table in self.buffer_dict[self.cursor_row]:
                token_string += table.token_ch
                token_all_width += table.token_width                
            
            if token_all_width > self.text_source_view.allocation.width - 200:
                self.text_source_view.set_size_request(token_all_width + self.text_view_padding_x + self.row_border_width + 500, 
                                                       self.text_source_view.allocation.height)
                    
            temp_padding_x = 0
            for table in self.buffer_dict[self.cursor_row]:
                if self.cursor_padding_x < temp_padding_x + table.token_width <= token_all_width:
                    break                
                else:
                    temp_padding_x += table.token_width
                    self.current_colume += 1
                    
    def get_ch_size(self, ch):
        if ch:
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 0, 0)
            cr = cairo.Context(surface)
            context = pangocairo.CairoContext(cr)
            layout = context.create_layout()
            layout.set_font_description(pango.FontDescription("%s %s" % (self.font_type, self.font_size)))
            layout.set_text(ch)
            return layout.get_pixel_size()
    
    ################################################    
    # Set attribute.        
    def __set_cursor_height(self, height):
        self.cursor_height = height
        
    def set_cursor_color(self, color="#000000"):
        self.cursor_color = color
        
    def get_font_size(self):    
        self.code_font_width, self.code_font_height = self.get_ch_size(" ")
        self.__set_cursor_height(self.code_font_height)
        
    def set_font_type(self, font_type):
        self.font_type = font_type
        self.get_font_size()
                
    def set_font_size(self, font_size):
        self.font_size = font_size
        self.get_font_size()
        
    def set_background_color(self, color="#FFFFFF"):
        self.bg_color = color
        
    def set_row_border_color(self, color="#F5F5F5"):
        self.row_border_color = color
        
    def set_code_line_color(self, color="#40E0D0"):
        self.code_line_color = color
        
    def set_code_line_alpha(self, alpha=0.2):
        self.code_line_alpha = alpha
        
    #################################################    
    # Tool function.    
    def color_to_rgb(self, color):
        if color[0] == '#': 
            gdk_color = gtk.gdk.color_parse(color)
            return (gdk_color.red / 65535.0, gdk_color.green / 65535.0, gdk_color.blue / 65535.0)
        
    #################################################    
    #     code edit text source view  function.     #
    #################################################    
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
                return " + ".join(key_modifiers) + " + " + key_name
        
    def key_press_event(self, widget, event):                        
        
        token_all_width = 0
        if self.buffer_dict.has_key(self.cursor_row):
            for table in self.buffer_dict[self.cursor_row]:
                token_all_width += table.token_width
                
            if token_all_width > self.text_source_view.allocation.width - 200:
                self.text_source_view.set_size_request(token_all_width + self.text_view_padding_x + self.row_border_width + 500, 
                                                       self.text_source_view.allocation.height)

        if self.current_row * self.code_font_height > self.text_source_view.allocation.height - 200:    
            self.text_source_view.set_size_request(self.text_source_view.allocation.width, 
                                                   self.current_row * self.code_font_height + 500)
                        
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
            
    #####################################################
    # keymap function.        
    #        
    def full_window(self):        
        top_window = self.window.get_toplevel()
        if top_window.get_state() == gtk.gdk.WINDOW_STATE_FULLSCREEN:
            top_window.unfullscreen()
        else:
            top_window.fullscreen()
        
    def Enter(self):        
        self.current_row += 1        
        self.current_colume = 0
        self.cursor_row += 1
        
        if not self.buffer_dict.has_key(self.current_row):
            self.buffer_dict[self.current_row] = []
            
        for temp_row in range(self.current_row, self.cursor_row, -1):
            if self.buffer_dict.has_key(temp_row - 1):
                for table in self.buffer_dict[temp_row-1]:
                    table.token_row = temp_row
                
                temp_buffer_dict = self.buffer_dict[temp_row-1]
                self.buffer_dict[temp_row] = temp_buffer_dict
                self.buffer_dict[temp_row - 1] = []

                        
        self.set_enter_last_string()            
        self.init_move_copy()    
        self.set_vadjustment()
        self.move_copy_bool = False
        
    def set_enter_last_string(self): 
        if self.buffer_dict.has_key(self.cursor_row - 1):
            temp_string = ""    
            temp_width  = 0
            temp_start_index = 0
            
            for table in self.buffer_dict[self.cursor_row-1]:    
                if temp_width == self.cursor_padding_x:
                    break
                else:
                    temp_width += table.token_width
                    temp_start_index += 1
                    
            for table in self.buffer_dict[self.cursor_row-1][temp_start_index:]:                                
                temp_table = Table()    
                temp_table.token_ch  = table.token_ch                
                temp_table.token_row = self.cursor_row
                temp_table.token_rgb = table.token_rgb
                self.buffer_dict[self.cursor_row].insert(len(self.buffer_dict[self.cursor_row]), temp_table)
                
                
            for index in range(0, temp_start_index):   
                temp_string += self.buffer_dict[self.cursor_row-1][index].token_ch
                
            self.buffer_dict[self.cursor_row-1] = []    
            
            for ch in temp_string:
                table = Table()
                table.token_ch = ch
                self.set_token_ch_color(ch, table)
                table.token_row = self.cursor_row - 1
                self.buffer_dict[self.cursor_row - 1].insert(len(self.buffer_dict[self.cursor_row-1]), table)
                
        self.cursor_padding_x = 0

        
    def Smart_Enter(self):        
        self.current_row += 1        
        self.current_colume = 0
        self.cursor_row += 1
        self.cursor_padding_x = 0
        
        if not self.buffer_dict.has_key(self.current_row):
            self.buffer_dict[self.current_row] = []
            
        for temp_row in range(self.current_row, self.cursor_row, -1):
            if self.buffer_dict.has_key(temp_row - 1):
                for table in self.buffer_dict[temp_row-1]:
                    table.token_row = temp_row
                
                temp_buffer_dict = self.buffer_dict[temp_row-1]
                self.buffer_dict[temp_row] = temp_buffer_dict
                self.buffer_dict[temp_row - 1] = []
            
        ##########################    
        # Set cursor position.
        self.set_cursor_position(self.cursor_row - 1)        
        # restart init move copy.
        self.init_move_copy()
        self.move_copy_bool = False                        
        self.set_vadjustment()
        self.queue_draw()        
        
    def set_cursor_position(self, cursor_row):
        if self.buffer_dict.has_key(cursor_row):
            for table in self.buffer_dict[cursor_row]:
                if table.token_ch == " ":
                    self.cursor_padding_x += table.token_width
                    temp_table = Table()
                    temp_table.token_ch = " "
                    temp_table.token_row = self.cursor_row
                    self.buffer_dict[self.cursor_row].insert(0, temp_table)
                    self.current_colume += 1
                else:    
                    break
                    
    def set_vadjustment(self):
        start_position_row = self.get_vadjustment().get_value() / self.code_font_height
        end_position_row   = self.allocation.height / self.code_font_height
        temp_row = end_position_row  + start_position_row
        if self.cursor_row >=  temp_row:
            # print "set_vadjustment.."
            self.get_vadjustment().set_value(self.get_vadjustment().get_value() + self.code_font_height)
            self.text_source_view.set_size_request(self.text_source_view.allocation.width,
                                                   self.text_source_view.allocation.height + self.code_font_height) 

    def Delete_Ch(self):            
        # return_up_row = True
        
        if self.buffer_dict.has_key(self.cursor_row):
            if self.buffer_dict[self.cursor_row]:
                delete_table = self.buffer_dict[self.cursor_row][self.current_colume-1]        
                self.cursor_padding_x -= delete_table.token_width
                self.buffer_dict[self.cursor_row].remove(delete_table)
                self.current_colume -= 1                
                # return_up_row = False
                
        # if return_up_row:                    
        #     self.current_row = max(self.current_row - 1, 1)
        #     self.cursor_row  = self.current_row
            
        self.queue_draw()    
        
    def Cursor_Up(self):        
        if self.cursor_row > 1:
            token_all_width = 0            
            if self.buffer_dict.has_key(self.cursor_row - 1):
                self.current_colume = 0
                for table in self.buffer_dict[self.cursor_row - 1]:
                    if token_all_width  >= self.cursor_padding_x:
                        break 
                    else:
                        token_all_width += table.token_width
                        self.current_colume += 1
                    
            self.cursor_row -= 1
            self.cursor_padding_x = token_all_width
            self.Cursor_Attr()
            
    def Cursor_Down(self):
        if self.cursor_row < self.current_row:            
            token_all_width = 0
            if self.buffer_dict.has_key(self.cursor_row + 1):
                self.current_colume = 0                
                for table in self.buffer_dict[self.cursor_row + 1]:
                    if token_all_width + table.token_width > self.cursor_padding_x:
                        break
                    else:                        
                        token_all_width += table.token_width
                        self.current_colume += 1
                    
            self.cursor_row += 1    
            self.cursor_padding_x = token_all_width
            self.Cursor_Attr()
            
    def Cursor_Left(self):
        if self.buffer_dict.has_key(self.cursor_row):
            if self.current_colume > 0:
                self.cursor_padding_x = self.cursor_padding_x - self.buffer_dict[self.cursor_row][self.current_colume - 1].token_width
                self.current_colume -= 1
                self.Cursor_Attr()
                
    def Cursor_Right(self):
        if self.buffer_dict.has_key(self.cursor_row):
            if self.current_colume < len(self.buffer_dict[self.cursor_row]):
                self.cursor_padding_x = self.cursor_padding_x + self.buffer_dict[self.cursor_row][self.current_colume].token_width
                self.current_colume += 1
                self.Cursor_Attr()
                
    def Cursor_Row_Start(self):
        self.cursor_padding_x = 0
        self.current_colume = 0
        self.Cursor_Attr()
        
    def Cursor_Row_End(self):
        if self.buffer_dict.has_key(self.cursor_row):
            for table in self.buffer_dict[self.cursor_row][self.current_colume:]:
                self.cursor_padding_x += table.token_width
                self.current_colume += 1            
        self.Cursor_Attr()    
        
    def Cursor_Attr(self):
        self.cursor_show_bool = True
        self.init_move_copy()
        self.move_copy_bool = False

        self.queue_draw()
        
    def Set_Tab(self):
        if self.Tab_BackSpace_Num:
            if not self.buffer_dict.has_key(self.cursor_row):
                self.buffer_dict[self.cursor_row] = []
                                        
            for num in range(0, self.Tab_BackSpace_Num):
                table = Table()
                table.token_ch = " "
                table.token_row = self.cursor_row
                w, h = self.get_ch_size(" ")
                self.cursor_padding_x += w                
                self.buffer_dict[self.cursor_row].insert(self.current_colume, table)
                self.current_colume += 1
            
    ###################################################            
                
    def get_text_view_focus_in(self, widget, event):    
        self.im.set_client_window(widget.window)        
        self.im.focus_in()
        
    def get_text_view_focus_out(self, widget, event):    
        self.im.focus_out()
        
    def expose_draw_text_source_view(self, widget, event):    
        cr = widget.window.cairo_create()
        rect = widget.allocation
        
        # Draw background.
        self.draw_text_source_view_background(cr, rect)
        # Draw code line.
        self.draw_text_source_view_code_line(cr, rect)        
        # Draw buffer string.
        self.draw_text_source_view_buffer_string(cr, rect)
        # Draw cursor.
        self.draw_text_source_view_cursor(cr, rect)        
        # Draw border.
        self.draw_text_source_view_border(widget, cr, rect)
        
        return True
    
    def get_press_cursor_position(self, widget, event, row):
        '''Get index at event.'''
        rect = widget.allocation
        cr = widget.window.cairo_create()
        context = pangocairo.CairoContext(cr)
        layout = context.create_layout()
        layout.set_font_description(pango.FontDescription("%s %s" % (self.font_size, self.font_size)))
        
        token_string = ""
        token_all_width = 0
        rect = widget.allocation        
        self.current_colume = 0
        
        for table in self.buffer_dict[row]:
            token_string += table.token_ch                
            temp_padding_x = token_all_width + self.row_border_width + self.text_view_padding_x
                
            if rect.x +  temp_padding_x < (event.x) < rect.x + temp_padding_x + table.token_width:                    
                break
            else:
                self.current_colume += 1
                token_all_width += table.token_width                                    
                    
        # print "(行:%s-列:%s)" % (row, self.current_colume)
        # Get left mouse clicked text view string postion.            
        
        return token_all_width
        
    def button_press_event(self, widget, event):
        row = int(event.y / self.code_font_height) + 1                
        
        if self.buffer_dict.has_key(row):
            token_all_width = self.get_press_cursor_position(widget, event, row)
        else:    
            token_all_width = 0
            
        if row <= self.current_row:
            if event.x < self.row_border_width + self.text_view_padding_x:
                token_all_width = 0
                self.current_colume = 0
                
            self.cursor_padding_x = token_all_width
            self.cursor_row  = row
            
        self.init_move_copy()
        
    def init_move_copy(self):        
        self.move_copy_bool = True        
        self.start_index_padding_x = 0
        self.end_index_padding_x = 0
        self.start_index = 0
        self.end_index = 0

    def draw_text_source_view_cursor(self, cr, rect):
        if self.cursor_show_bool:
            cr.set_source_rgb(*self.color_to_rgb(self.cursor_color))        
            cr.rectangle(rect.x + self.row_border_width + self.text_view_padding_x + self.cursor_padding_x,
                         rect.y + (self.cursor_row - 1) * self.cursor_height,
                         1,
                         self.cursor_height)
            cr.fill()
        
    def draw_text_source_view_buffer_string(self, cr, rect):        
        # Draw current cursor show position(rectangle).
        self.draw_text_source_view_rectangle(cr, rect)
        
        context = pangocairo.CairoContext(cr)            
        layout = context.create_layout()
        layout.set_font_description(pango.FontDescription("%s %s" % (self.font_type, self.font_size)))        
        (text_width, text_height) = layout.get_pixel_size()            
        
        save_colume_all_width = 0        
        
        start_position_row = int(self.get_vadjustment().get_value() / self.code_font_height)
        end_position_row   = int(self.allocation.height / self.code_font_height)
        temp_row = end_position_row  + start_position_row
        
        if temp_row > self.current_row + 1:
            temp_row = self.current_row + 1
            
        for key in range(start_position_row, temp_row + 1):            
                save_colume_all_width = 0
                if self.buffer_dict.has_key(key):
                    for table in self.buffer_dict[key]:

                        layout.set_text(table.token_ch)
                
                        self.code_font_width, self.code_font_height = layout.get_pixel_size()
                
                        # Set font position.
                        x_padding = rect.x + self.row_border_width + self.text_view_padding_x + save_colume_all_width    
                        cr.move_to(x_padding, 
                                   rect.y + (table.token_row - 1) * self.code_font_height)
                
                        save_colume_all_width += self.code_font_width
            
                        # Save font size.
                        table.token_width  = self.code_font_width
                        table.token_height = self.code_font_height
                        # Set font rgb.
                        cr.set_source_rgb(*self.color_to_rgb(table.token_rgb))
                        # Show font.
                        context.update_layout(layout)
                        context.show_layout(layout)        

        # self.draw_text_source_view_move_copy(cr, rect)        
        
    def draw_text_source_view_move_copy(self, cr, rect):    
        rgb = self.color_to_rgb(self.move_copy_color)
        cr.set_source_rgba(rgb[0], rgb[1], rgb[2], self.move_copy_alpha)
        
        temp_x = rect.x + self.text_view_padding_x + self.row_border_width + self.start_index_padding_x
        
        temp_width = self.end_index_padding_x - self.start_index_padding_x
        cr.rectangle(
            temp_x,
            rect.y + (self.cursor_row - 1) * self.code_font_height,
            temp_width,
            self.code_font_height
            )
        cr.fill()
        
    def draw_text_source_view_rectangle(self, cr, rect):        
        rgb  = self.color_to_rgb(self.text_view_rectangle_color)
        cr.set_source_rgba(rgb[0], rgb[1], rgb[2], self.text_view_rectangle_alpha)   
        cr.rectangle(rect.x + self.text_view_padding_x + self.border_width, 
                     rect.y + (self.cursor_row-1) * self.code_font_height, 
                     rect.width - self.text_view_padding_x + self.border_width, 
                     self.code_font_height)
        cr.fill()

    
    def draw_text_source_view_background(self, cr, rect):
        cr.set_source_rgb(*self.color_to_rgb(self.bg_color))
        cr.rectangle(rect.x + self.row_border_width - 1,
                     rect.y,
                     rect.width - self.row_border_width + 1,
                     rect.height)
        cr.fill()
        
        
    def draw_text_source_view_border(self, widget, cr, rect):    
        coordinate = widget.translate_coordinates(self, rect.x, rect.y)
        offset_x, offset_y = coordinate

        cr.set_source_rgb(*self.color_to_rgb(self.row_border_color))
        cr.rectangle(-offset_x,
                     rect.y,
                     self.row_border_width,
                     rect.height)
        cr.fill()                                        
        
        # Draw code folding.
        self.draw_text_source_view_code_folding(cr, rect, offset_x)
        
        #Draw row number.
        self.draw_text_source_view_row_number(cr, rect, offset_x)
        
        if self.expose_row_border_bool:
            self.queue_draw_area(-offset_x, 
                                  rect.y,
                                  self.row_border_width + self.text_view_padding_x,
                                  rect.height)
            
    def draw_text_source_view_row_number(self, cr, rect, offset_x):
        rgb = self.color_to_rgb(self.code_number_color)
        cr.set_source_rgba(rgb[0], rgb[1], rgb[2], self.code_number_alpha)
        
        start_position_row = int(self.get_vadjustment().get_value() / self.code_font_height)                
        end_position_row   = int(self.allocation.height / self.code_font_height) + 1
        temp_row = end_position_row  + start_position_row
        
        if temp_row > self.current_row +1:
            temp_row = self.current_row + 1
            
        for row_number in range(start_position_row+1, temp_row):

            context = pangocairo.CairoContext(cr)            
            layout = context.create_layout()
            
            temp_font_size = self.font_size
            if row_number == self.cursor_row:
                temp_font_size += 1     
                
            layout.set_font_description(pango.FontDescription("%s %s" % (self.font_type, temp_font_size)))        
            (text_width, text_height) = layout.get_pixel_size()            
            
            layout.set_text(str(row_number))
            cr.move_to(
                -offset_x + rect.x + self.text_view_padding_x + self.border_width + self.code_number_padding_x,
                rect.y + (row_number - 1) * self.code_font_height
                )
            context.update_layout(layout)
            context.show_layout(layout)
            
            
    def draw_text_source_view_code_line(self, cr, rect):
        rgb = self.color_to_rgb(self.code_line_color)        
        cr.set_source_rgba(rgb[0], rgb[1], rgb[2], self.code_line_alpha)
        cr.rectangle(rect.x + self.code_line_padding_x, 
                     rect.y,
                     1,
                     rect.y + rect.height)
        cr.fill()
        
    def draw_text_source_view_code_folding(self, cr, rect, offset_x):            
        temp_code_folding_x = 3
        rgb = self.color_to_rgb("#FFFFFF")
        cr.set_source_rgb(*rgb)

        code_folding_x = rect.x + self.row_border_width 
        # draw code folding background.
        cr.rectangle(-offset_x +  code_folding_x,
                      rect.y,
                      self.text_view_padding_x,
                      rect.y + rect.height)
        cr.fill()
        # draw code folding line.        
        rgb = self.color_to_rgb(self.code_folding_color)
        cr.set_source_rgba(rgb[0], rgb[1], rgb[2], self.code_folding_alpha)
        self.code_folding_height = self.current_row * self.code_font_height
        cr.rectangle(-offset_x +  code_folding_x + (self.text_view_padding_x - temp_code_folding_x)/2,
                     rect.y,
                     1,
                     rect.y + self.code_folding_height)
        cr.fill()        
        
        # # draw code folding min rectangle.        
        # cr.rectangle(-offset_x +  code_folding_x,
        #               rect.y,
        #               self.text_view_padding_x - temp_code_folding_x,
        #               self.text_view_padding_x - temp_code_folding_x)
        # cr.stroke()
        
    def read(self, file_path):
        
        if os.path.exists(file_path):
            self.read_file(file_path)
        else:    
            self.perror("讀取文件錯誤!!")
                    
        gtk.timeout_add(800, self.set_read_time)
        
    def set_read_time(self):    
        self.Cursor_Row_End()
        return False
    
    def read_file(self, file_path):
        fp = open(file_path, "r")
        temp_row = self.current_row
        # temp_buffer = {}
        text = fp.read().decode("utf-8")
        fp.close()                

        for ch in text:            
            if ch == "\n":                
                temp_row += 1
                self.current_colume = 0
                continue                            
            
            table = Table()
            table.token_ch = ch
            self.set_token_ch_color(ch, table)
            table.token_row = temp_row            
            
            
            if not self.buffer_dict.has_key(temp_row):
                self.buffer_dict[temp_row] = []
                
            self.buffer_dict[temp_row].insert(self.current_colume, table)
            self.current_colume += 1
            
        self.buffer_dict[temp_row] = [] # delete last
        self.current_row = temp_row - 1
        self.current_colume = 0
        self.queue_draw()
        
    def perror(self, string):
        print "====", string, "====="
        
class Buffer(object):        
    def __init__(self):
        pass

    
class Table(object):        
    def __init__(self):
        self.token_ch      = ""
        self.token_rgb     = "#000000" # (r, g, b)
        self.token_width   = 0
        self.token_height  = 0
        self.token_row     = 0
        self.token_column  = 0
    

if __name__ == "__main__":        
    class Test(object):
        def __init__(self):
            self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
            self.win.set_size_request(500, 500)
            self.win.connect("destroy", gtk.main_quit)
            self.code_edit = CodeEdit()
            self.code_edit.read("/home/long/123.txt")
            # self.hbox = gtk.VBox()
            # self.hbox.pack_start(CodeEdit())
            # self.hbox.pack_start(self.code_edit)
            # self.win.add(self.hbox)
            self.win.add(self.code_edit)
            self.win.show_all()
            

    Test()            
    gtk.main()    
    
