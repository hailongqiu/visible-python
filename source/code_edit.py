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
from regex import Scan

MOVE_COPY_STATE_MID   = 0
MOVE_COPY_STATE_LEFT  = 1
MOVE_COPY_STATE_RIGHT = 2

class CodeEdit(gtk.ScrolledWindow):
    def __init__(self,
                 buffer=None):
        gtk.ScrolledWindow.__init__(self)
        #######################################
        ###
        # self.scan = Scan("language/python.ini")
        self.scan_file_ini = "language/python.ini"
        #######################################
        ### init imm.
        '''Init IMMulticontext.'''
        self.im = gtk.IMMulticontext()
        self.im_offset_x = 0
        self.im_offset_y = 0
        self.im.connect("commit", self.get_im_input_string)
        #######################################
        ### init value.
        '''Init font type/size.'''
        self.font_type  = "文泉驿等宽微米黑"
        self.font_size  = 11
        '''Init value.'''
        self.buffer = []
        self.temp_buffer = Buffer()
        self.buffer_dict = OrderedDict
        self.buffer_dict = {}
        self.current_row    = 1
        self.current_colume = 0
        self.row_border_width = 70                
        self.expose_row_border_bool = False
        self.text_view_padding_x = 15
        # read file.
        self.file_path = None
        '''Init Operation.''' # 123456
        self.start_row       = 0
        self.end_row         = 0
        self.start_index     = 0
        self.end_index       = 0
        self.start_index_padding_x   = 0
        self.end_index_padding_x     = 0        
        self.move_copy_bool  = False
        self.move_copy_draw_bool = False
        self.move_copy_color = "#778899"
        self.move_copy_alpha = 0.4
        self.move_copy_state = MOVE_COPY_STATE_MID
        '''Init code number.'''
        self.code_number_color = "#000000"
        self.code_number_alpha = 0.3
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
        '''Init compile.'''
        self.compile_cmd = "python"
        '''Init keymap.'''
        self.keymap = {
            # "F5":self.run_compile,
            "Tab":self.Set_Tab,
            # "Ctrl + /":self.Revoke,
            # "Ctrl + ?":self.Cancel_Revoke,
            "Ctrl + w":self.clipboard_cut,
            "Alt + w":self.clipboard_c,
            "Ctrl + y":self.clipboard_v,
            "Ctrl + a":self.Cursor_Row_Start,
            "Ctrl + e":self.Cursor_Row_End,
            "Ctrl + f":self.Cursor_Right,
            "Ctrl + b":self.Cursor_Left,
            "Ctrl + p":self.Cursor_Up,
            "Ctrl + n":self.Cursor_Down,
            "Ctrl + s":self.save_to_file,
            "F11":self.full_window,
            "Return":self.Enter,
            "Ctrl + l":self.Smart_Enter,
            "BackSpace":self.Delete_Ch
            }
        ########################################
        ### text_source_view.
        '''Init text_source_view.'''
        self.text_source_view = gtk.Button()
        # self.text_source_view.set_size_request(888, 800)
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
        
        self.set_im_position(0, 0)
        # gtk.timeout_add(self.cursor_time, self.set_cursor_show_bool_time)
        
        # test plugins.
        module = __import__('plugins.%s'%("devhelp"),
                   fromlist=["devhelp"])
        print module
        getattr(module, "devhelp")(self)
        
    #############################    
    ### im input position.
    def set_im_position(self, x1, y2):    
        x = self.text_source_view.allocation.x + self.row_border_width + self.text_view_padding_x + x1
        self.im.set_cursor_location((x,
                                     0, 0, 
                                     self.code_font_height - 5 + y2))
        
    def set_cursor_show_bool_time(self):
        self.cursor_show_bool = not self.cursor_show_bool
        self.queue_draw()
        return True
    
    def button_release_event(self, widget, event):
        print "button_release_event"
        self.move_copy_bool = False
        
    def motion_notify_event(self, widget, event):  # 123456
        #################################
        if self.move_copy_bool:
            # Get mouse move row.
            move_row = int(event.y / self.code_font_height) + 1
            min_row =  int(self.get_vadjustment().get_value() / self.code_font_height)
            max_row =  int(self.allocation.height / self.code_font_height)
            
            temp_row = int(min_row + max_row)
            self.end_row = min(min(move_row, temp_row), self.current_row)
            
            if self.start_row == self.end_row:
                self.move_copy_state = MOVE_COPY_STATE_MID
            elif self.start_row > self.end_row:    
                self.move_copy_state = MOVE_COPY_STATE_LEFT
            elif self.start_row < self.end_row:    
                self.move_copy_state = MOVE_COPY_STATE_RIGHT
                
            self.end_index_padding_x = self.get_motion_cursor_position(widget, event, self.end_row)
            self.cursor_padding_x    = self.end_index_padding_x
            self.cursor_row = self.end_row
            self.end_index  = self.current_colume
            self.move_copy_draw_bool = True
        ###################################    
        self.queue_draw()
        
    def get_motion_cursor_position(self, widget, event, row):    
        return self.get_press_cursor_position(widget, event, row)
    
    def scrolled_window_value_changed(self, adjustment):  
        self.expose_row_border_bool = True
        self.text_source_view.queue_draw()
        
    def scrolled_window_vadjustment_value_changed(self, vadjustment):    
        self.expose_row_border_bool = False
        self.text_source_view.queue_draw()
        
    ################################################        
    # Set imm.    
    def get_im_input_string(self, IMMulticontext, text):
        
        # SAve buffer.
        # import copy
        # self.temp_buffer.save_temp_buffer(copy.copy(self.buffer_dict))

        text_utf_8 = text.decode('utf-8')
        
        for ch in text_utf_8:
            table = Table()
            table.token_ch = ch
            table.token_width, table.token_height = self.get_ch_size(ch)
            table.token_row = self.cursor_row
                                    
            if self.buffer_dict.has_key(self.cursor_row):
                self.buffer_dict[self.cursor_row].insert(self.current_colume, table)
            else:
                self.buffer_dict[self.cursor_row] = []
                self.buffer_dict[self.cursor_row].insert(0, table)
                                
            self.cursor_padding_x += self.get_ch_size(ch)[0]
            
            # get current cursor position.  
            self.get_current_cursor_colume()
                    
            self.set_im_position(
                0,
                (self.cursor_row - 1) * self.code_font_height)    
                                    
                            
        self.set_token_text_color(self.cursor_row)
        self.expose_area_input_text()
        
    def expose_area_input_text(self):    
        self.cursor_show_bool = True
        self.move_copy_draw_bool = False
        self.move_copy_bool = False
        self.set_im_position(
            0,
            (self.cursor_row - 1) * self.code_font_height)    

        rect = self.text_source_view.allocation        
        paner_rect = self.allocation
        start_position_row = int(self.get_vadjustment().get_value() / self.code_font_height)
        self.queue_draw_area(rect.x,
                             rect.y + (self.cursor_row - start_position_row - 1) * self.code_font_height - self.code_font_height,
                             paner_rect.width,
                             self.code_font_height * 2 + self.code_font_height/2)

    def set_token_text_color(self, row):            
        temp_text = ""
        for table in self.buffer_dict[row]:
            temp_text += table.token_ch
            
        temp_text = temp_text.decode("utf-8")
        
        scan = Scan(self.scan_file_ini)        
        for i in scan.scan(temp_text, row):
            for colume in range(i.start_index, i.end_index+1):
                self.buffer_dict[i.row][colume].token_rgb = str(i.rgb)
                
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
                if key_name == " ":
                    key_name = "Space"
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
        self.Cursor_Attr()
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
                table.token_row = self.cursor_row - 1
                self.buffer_dict[self.cursor_row - 1].insert(len(self.buffer_dict[self.cursor_row-1]), table)                
                
            # modify enter line color(rgb).    
            self.set_token_text_color(self.cursor_row - 1)
            
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
        self.Cursor_Attr()
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
        if self.move_copy_draw_bool:
            self.clipboard_cut()
        else:    
            token_all_width = self.del_row_colume_to_end_text(self.cursor_row, max(self.current_colume-1, 0), self.current_colume)
            self.current_colume = max(self.current_colume - 1, 0)
            self.cursor_padding_x -= token_all_width
            
            if not token_all_width and self.cursor_row > 1:                
                ##########################################
                temp_width = 0
                temp_colume = 0
                for table in self.buffer_dict[self.cursor_row]:
                    table.token_row = self.cursor_row - 1
                    self.buffer_dict[self.cursor_row - 1].append(table)
                    temp_width += table.token_width
                    temp_colume += 1
                    
                self.buffer_dict[self.cursor_row] = []
                self.up_move_row_text(self.cursor_row)
                ###########################################
                self.cursor_row -= 1
                token_all_width = 0
                self.current_colume = 0
                if not self.buffer_dict.has_key(self.cursor_row):
                    self.buffer_dict[self.cursor_row] = []
                    
                for table in self.buffer_dict[self.cursor_row]:
                    token_all_width += table.token_width                    
                    self.current_colume += 1
                self.cursor_padding_x = token_all_width  - temp_width
                self.current_colume -= temp_colume
                #############################################
            self.Cursor_Attr()
            
        self.set_token_text_color(self.cursor_row)    
        
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
            
            temp_padding_value = 8
            if self.cursor_row <= self.get_expose_start_and_end_row()[0] + temp_padding_value: 
                temp_value = self.get_expose_start_and_end_row()[0] - self.cursor_row + temp_padding_value
                self.get_vadjustment().set_value(self.get_vadjustment().get_value() - temp_value * self.code_font_height)
            elif self.cursor_row >= self.get_expose_start_and_end_row()[2]:
                '''self.cursor_row - start_position_row'''
                temp_value = self.cursor_row - self.get_expose_start_and_end_row()[0] - 1
                self.get_vadjustment().set_value(self.get_vadjustment().get_value() + temp_value * self.code_font_height)
                
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
                        
            temp_padding_row = 8
            
            # [2] -> temp_row ( start_position_row + end_position_row)
            if self.cursor_row >= self.get_expose_start_and_end_row()[2] - temp_padding_row:
                temp_value = self.cursor_row - self.get_expose_start_and_end_row()[2] + temp_padding_row
                self.get_vadjustment().set_value(self.get_vadjustment().get_value() + temp_value * self.code_font_height)
            elif self.cursor_row < self.get_expose_start_and_end_row()[0]:     
                # temp_padding_value = 2
                '''(start_position_row + end_position_row) - cursor_row'''
                temp_value = self.get_expose_start_and_end_row()[2] -  self.cursor_row - temp_padding_row
                self.get_vadjustment().set_value(self.get_vadjustment().get_value() - temp_value * self.code_font_height)
                
            self.Cursor_Attr()                          
            
    def get_expose_start_and_end_row(self):
        start_position_row = self.get_vadjustment().get_value() / self.code_font_height
        end_position_row   = int(self.allocation.height-10) / self.code_font_height
        temp_row = int(end_position_row  + start_position_row)
        return int(start_position_row), int(end_position_row), temp_row
        
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
        self.move_copy_draw_bool = False
        self.move_copy_bool = False
        # self.queue_draw()
        rect = self.allocation
        self.queue_draw_area(rect.x,
                             rect.y,
                             rect.width,
                             rect.height)
        self.set_im_position(
            0,
            (self.cursor_row - 1) * self.code_font_height)    

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
            
    # def Cancel_Revoke(self):        
    #     self.buffer_dict = self.temp_buffer.next()
    #     self.queue_draw()
        
    # def Revoke(self):    
    #     self.buffer_dict = self.temp_buffer.pre()
    #     self.queue_draw()
        
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
        
        # token_string = ""
        token_all_width = 0
        rect = widget.allocation        
        temp_padding_x =  self.row_border_width + self.text_view_padding_x
        self.current_colume = 0
        if event.x < temp_padding_x:            
            return 0

        if self.buffer_dict.has_key(row):
            for table in self.buffer_dict[row]:                
                # token_string += table.token_ch
                if (rect.x +  temp_padding_x + token_all_width) <= (event.x) <= (rect.x + temp_padding_x + token_all_width + table.token_width):                    
                    break
                else:
                    self.current_colume += 1
                    token_all_width += table.token_width                            
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
            
        self.move_copy_draw_bool = False    
        self.init_move_copy()        
        
        
    def init_move_copy(self):        
        self.move_copy_bool = True
        self.start_index_padding_x = self.cursor_padding_x
        self.end_index_padding_x   = self.cursor_padding_x
        self.start_index = self.current_colume
        self.end_index   = self.current_colume
        self.start_row = self.cursor_row
        self.end_row   = self.cursor_row
        
        self.set_im_position(0, 
                             (self.cursor_row - 1) * self.code_font_height)

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
                        
        if self.move_copy_draw_bool:
            self.draw_text_source_view_move_copy(cr, rect)        
        
    def draw_text_source_view_move_copy(self, cr, rect):  # 123456        
        rgb = self.color_to_rgb(self.move_copy_color)
        cr.set_source_rgba(rgb[0], rgb[1], rgb[2], self.move_copy_alpha)
        
        temp_x         = rect.x + self.text_view_padding_x + self.row_border_width
        temp_y         = rect.y 
        temp_width     = 0
        temp_padding_x = 0
        temp_start_row = self.start_row
        temp_end_row   = self.end_row
        
        if temp_start_row > temp_end_row:
            temp_row       = temp_end_row
            temp_end_row   = temp_start_row
            temp_start_row = temp_row
            temp_start_row -= 1
            temp_end_row   += 0
        else:    
            temp_end_row   += 0
            temp_start_row -= 1
        
        if self.move_copy_state == MOVE_COPY_STATE_MID:
            temp_padding_width = self.end_index_padding_x - self.start_index_padding_x 
            cr.rectangle(
                temp_x + self.start_index_padding_x,
                temp_y + (self.cursor_row - 1) * self.code_font_height,
                temp_padding_width,
                self.code_font_height
                )
            cr.fill()
        else:                
            for row in range(temp_start_row, temp_end_row):                
                ##################################################
                ### Draw first and last.
                if row == temp_start_row:                                        
                    if self.move_copy_state   == MOVE_COPY_STATE_LEFT: # start > end
                        temp_padding_x = self.end_index_padding_x
                        temp_width = rect.width - self.end_index_padding_x
                    elif self.move_copy_state == MOVE_COPY_STATE_RIGHT:
                        temp_padding_x = self.start_index_padding_x                        
                        temp_width = rect.width - self.start_index_padding_x
                elif row == temp_end_row - 1:                                    
                    if self.move_copy_state   == MOVE_COPY_STATE_LEFT: # start > end
                        temp_padding_x = 0
                        temp_width = self.start_index_padding_x
                    elif self.move_copy_state == MOVE_COPY_STATE_RIGHT: # start < end
                        temp_padding_x = 0
                        temp_width     = self.end_index_padding_x
                else:        
                    temp_width     = rect.width
                    temp_padding_x = 0
                ##################################################
                ### Draw rectangle.
                cr.rectangle(
                    temp_x + temp_padding_x, 
                    temp_y + (row) * self.code_font_height,
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
        
    ###############################################    
    ### Operation buffer.
    ###    
    def clipboard_attr(self):
        self.cursor_show_bool = True
        self.move_copy_draw_bool = False
        self.move_copy_bool = False
        self.queue_draw()
    
    def clipboard_cut(self):                                 
        if self.move_copy_draw_bool:
            # last text to first text.        
            if self.start_row == self.end_row:
                move_cursor_bool = True
                if self.start_index > self.end_index:
                    temp_index = self.end_index
                    self.end_index = self.start_index
                    self.start_index = temp_index                
                    move_cursor_bool = False
                
                token_all_width = self.del_row_colume_to_end_text(self.start_row, self.start_index, self.end_index)            
                
                if move_cursor_bool:
                    self.cursor_padding_x -= token_all_width 
                    self.current_colume = self.current_colume - (self.end_index - self.start_index)# 123456
            else:    
                # Sawp start and end row.
                if self.start_row > self.end_row:
                    temp_row = self.end_row
                    self.end_row = self.start_row
                    self.start_row = temp_row                                    
                    
                for row in range(self.start_row, self.end_row + 1):            
                    # for colume in range()
                    if row == self.start_row:  # first.
                        if self.move_copy_state == MOVE_COPY_STATE_RIGHT:
                            self.del_row_colume_to_end_text(row, self.start_index, len(self.buffer_dict[row]))
                        elif self.move_copy_state == MOVE_COPY_STATE_LEFT:
                            if self.end_index:
                                self.del_row_colume_to_end_text(row, self.end_index, len(self.buffer_dict[row]))
                            else:    
                                self.buffer_dict[row] = []                                
                    elif row == self.end_row:    # last.
                        if self.move_copy_state == MOVE_COPY_STATE_RIGHT:                            
                            self.del_row_colume_to_end_text(row, 0, self.end_index)
                            #######################
                            ### get first row 0 - start index width.
                            o_to_start_index_width = 0
                            self.current_colume = 0
                            for colume in range(0, self.start_index):
                                width = self.buffer_dict[self.start_row][colume].token_width
                                o_to_start_index_width += width
                                self.current_colume = 0
                            ##### Set cursor position.    
                            self.cursor_row = self.start_row
                            self.cursor_padding_x = o_to_start_index_width
                            #############################
                        elif self.move_copy_state == MOVE_COPY_STATE_LEFT:    
                            self.del_row_colume_to_end_text(row, 0, self.start_index)
                        self.end_text_to_first_text(row, self.start_row)
                    else:#  
                        # self.del_row_colume_to_end_text(row, 0, len(self.buffer_dict[row]))                            
                        self.buffer_dict[row] = []
                        
                temp_start_row = self.start_row        
                if self.buffer_dict[self.start_row]:        
                    temp_start_row = self.start_row + 1
                    
                for row in range(self.end_row , temp_start_row - 1, -1):        
                    #up move row text.
                    self.up_move_row_text(row)
                
            self.Cursor_Attr()
            
    def up_move_row_text(self, row):                
        temp_buffer_dict = []
        for row in range(row, self.current_row):
            temp_buffer_dict = self.buffer_dict[row]
            self.buffer_dict[row] = self.buffer_dict[row + 1]
            self.buffer_dict[row + 1] = temp_buffer_dict
            
            for table in self.buffer_dict[row]:
                table.token_row = row                

        self.current_row = max(self.current_row - 1, 1)
            
    def end_text_to_first_text(self, row, type_row):        
        #######Save row buffer_dict###########
        temp_table = []
        for table in self.buffer_dict[row]:
            table.token_row = type_row
            temp_table.append(table)
        ######################################    
        self.buffer_dict[row] = []
        ######################################
        # temp_text to first text.
        for table in temp_table:
            self.buffer_dict[type_row].append(table)
        ######################################
        
    def del_row_colume_to_end_text(self, row, start_index, end_index):    
        import copy
        temp_buffer_dict = copy.copy(self.buffer_dict[row])
        token_all_width = 0
        for colume in range(start_index, end_index):
            token_all_width += self.buffer_dict[row][colume].token_width
            temp_buffer_dict.remove(self.buffer_dict[row][colume])            
        self.buffer_dict[row] = temp_buffer_dict

        return token_all_width
    
    def clipboard_c(self):
        pass
    
    def clipboard_v(self):
        clipboard = gtk.Clipboard()
        clipboard.request_text(self.get_clipboard_text)
        
    def get_clipboard_text(self, clipboard, text, data):    
        if text:
            text = text.decode("utf-8")
            if text[-1] == "\n":
                text = text[:-1]
            
            v_text_list = text.split("\n")
            temp_row = self.cursor_row # save row.
            temp_colume = self.current_colume # save colume.
            
            num_list = len(v_text_list) - 1
            
            if num_list > 0:
                for row in range(self.current_row + 1,
                                 self.current_row + num_list + 1):
                    self.buffer_dict[row] = []
                    
                for row in range(self.current_row + num_list, 
                                 temp_row + num_list, -1):
                    self.buffer_dict[row] = []
                    self.buffer_dict[row] = self.buffer_dict[row - num_list]
                    self.buffer_dict[row - num_list] = []
                    for colume in range(0, len(self.buffer_dict[row])):
                        self.buffer_dict[row][colume].token_row = row
                                                                                                    
                # delete cursor row last text(string).
                import copy
                buffer_dict_row = copy.copy(self.buffer_dict[temp_row])                
                for colume in range(temp_colume, len(buffer_dict_row)):
                    v_text_list[num_list] += (buffer_dict_row[colume].token_ch)
                    self.buffer_dict[temp_row].remove(buffer_dict_row[colume])
                    
                self.current_row += num_list
                
            ###########################################    
            ## move row.    
            for v_text in v_text_list:
                for ch in v_text:
                    table = Table()
                    table.token_ch = ch
                    table.token_width, table.token_height = self.get_ch_size(ch)
                    table.token_row = temp_row 
                    temp_colume += 1
                    self.buffer_dict[temp_row].insert(temp_colume-1, table)                    
                    
                temp_row += 1
                                        
            self.Cursor_Attr()
            
    def run_compile(self):    
        os.system(self.compile_cmd + " %s"%(self.file_path))
        
    def save(self, file_path):    
        if os.path.exists(file_path):
            self.save_file(file_path)
        else:    
            self.perror("保存文件错误!!")
            
    def save_to_file(self):
        self.save(self.file_path)        
        
    def save_file(self, file_path):                
        read_fp = open(self.file_path, "r")
        read_text = read_fp.read().decode("utf-8")
        read_fp.close()

        read_text_list = read_text.split("\n")

        for key in self.buffer_dict.keys():            
            if key <= self.current_row:
                text = ""
                for table in self.buffer_dict[key]:
                    text += table.token_ch 
                    
                try:    
                    if read_text_list[key - 1] != text:
                        read_text_list[key - 1] = text
                except:
                    read_text_list.append(text)                    
        
        read_text = "\n".join(read_text_list)
        
        write_fp = open(file_path, "w")
        write_fp.write(read_text)
        write_fp.close()
        
    def read(self, file_path):        
        if os.path.exists(file_path):
            self.read_file(file_path)            
        else:    
            self.perror("讀取文件錯誤!!")            
            self.current_row = 1        
            
    def read_file(self, file_path):
        self.file_path = file_path        
        fp = open(self.file_path, "r")
        text = fp.read().decode("utf-8")
        fp.close()
        
        self.text_list = text.split("\n")
        
        self.sum_row = max(len(self.text_list) - 1, 1)
        self.row_next = 0
        max_colume = 0

        if self.sum_row > 1000:
            self.row_next = 1000
            gtk.timeout_add(500, self.read_max_file_time)
        else:    
            self.row_next = self.sum_row
            
        # first read file init.        
        for row in range(0, self.row_next):
            self.buffer_dict[row + 1] = []
            self.current_colume = 0
            
            for ch in self.text_list[row]:
                table = Table()
                table.token_ch = ch
                table.token_row = row + 1
                
                self.buffer_dict[row + 1].insert(self.current_colume, table)
                self.current_colume += 1
                
                if self.current_colume > max_colume:
                    max_colume = self.current_colume
                    
        self.current_row = self.row_next
                
        # Set height and width(text_source_view size).
        text_source_view_padding_height = 50
        text_source_view_padding_width  = 200
        self.text_source_view.set_size_request(max_colume * self.code_font_width + text_source_view_padding_width,
                                               self.sum_row * self.code_font_height + text_source_view_padding_height)
        self.Cursor_Attr()
        
        
    def read_max_file_time(self):    
        max_colume = 0
        read_start = self.row_next
        if (self.row_next + 1000) > self.sum_row:
            read_end = self.sum_row
        else:    
            self.row_next += 1000
            read_end   = self.row_next
        
        # first read file init.
        for row in range(read_start, read_end):
            self.buffer_dict[row + 1] = []
            self.current_colume = 0
            for ch in self.text_list[row]:
                table = Table()
                table.token_ch = ch
                table.token_row = row + 1
                
                self.buffer_dict[row + 1].insert(self.current_colume, table)                
                self.current_colume += 1
                
                if self.current_colume > max_colume:
                    max_colume = self.current_colume
                    
        self.current_row = read_end
        # set width and height.            
        text_source_view_padding_height = 50
        text_source_view_padding_width  = 200                    
        self.text_source_view.set_size_request(max_colume * self.code_font_width + text_source_view_padding_width,
                                               self.sum_row * self.code_font_height + text_source_view_padding_height)
                    
        if read_end == self.sum_row:
            return False
        return True
    
    
    def perror(self, string):
        print "====", string, "====="        
        


class Buffer(object):
    '''Init buffer.'''
    def __init__(self):
        self.save_buffer = []
        self.index = -1
        self.__BUFFER_MAX_NUM = 5
        
    def save_temp_buffer(self, buffer_dict):        
        if len(self.save_buffer) <= self.__BUFFER_MAX_NUM:
            self.save_buffer.append(buffer_dict)
            self.index += 1
            print self.index
            
    def next(self): # ctrl + Z
        if self.index +1 <= len(self.save_buffer) - 1:
            self.index += 1
            temp_save_buffer = self.save_buffer[self.index]            
            return temp_save_buffer
        
    def pre(self): # Ctrl + z
        if self.index != -1:
            if self.index >= 0:
                temp_save_buffer = self.save_buffer[self.index]
                self.index -= 1
                return temp_save_buffer                
        
    
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
            # self.code_edit.read("/home/long/123.py")
            # self.hbox = gtk.VBox()
            # self.hbox.pack_start(CodeEdit())
            # self.hbox.pack_start(self.code_edit)
            # self.win.add(self.hbox)
            self.win.add(self.code_edit)
            self.win.show_all()
            

    Test()            
    gtk.main()    
    
