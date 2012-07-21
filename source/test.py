#coding:utf-8

from dtk.ui.utils import get_match_parent
import gtk
import pangocairo
import pango
import cairo

class CodeEdit(gtk.ScrolledWindow):        
    def __init__(self):
        gtk.ScrolledWindow.__init__(self)
        '''Set attr.'''
        self.set_size_request(300, 300)
        '''Init IMMulticontext.'''
        self.im = gtk.IMMulticontext()
        self.im.connect("commit", self.test_add_buffer_text)
        self.imm_x = 70
        self.imm_y = 0
        self.set_im_position()

        '''Init value.'''
        self.ajustment_value = 0
        self.expoe_bool     = False
        self.current_row    = 0
        self.current_column = 1
        self.h_ajustment_padding_w    = 0 # move border(show row number toolbar)
        # font string value.
        self.code_font_width  = 0
        self.code_font_height = 0
        # cursor value.
        self.cursor_draw_all_width  = 0
        self.cursor_draw_bool       = True
        self.cursor_position_x      = 0
        self.cursor_position_y      = 0
        self.cursor_position_row    = 0
        self.cursor_position_column = 0
        self.cursor_position_width  = 0
        self.cursor_position_height = 0
        self.cursor_show_time       = 800
        # init font.
        self.font_type  = "文泉驿微米黑"
        self.font_size  = 12
        # init Table.
        self.tables = []
        self.test_string()        
        '''Init widget.'''
        self.code_edit_text_view  = gtk.Button()
        self.code_edit_text_view.set_can_focus(True)
        self.code_edit_text_view.grab_focus()        

        self.code_edit_text_view.set_size_request(500, 500)
        self.add_with_viewport(self.code_edit_text_view)
        '''Init events.'''
        # Init code edit ScrolledWindow events.
        # self.get_hadjustment().connect("value-changed", self.scrolled_window_value_changed)        
        # Init code edit events.       
        self.code_edit_text_view.add_events(gtk.gdk.ALL_EVENTS_MASK)        
        self.code_edit_text_view.connect("expose-event",          self.expose_code_edit_text_view)
        self.code_edit_text_view.connect("motion-notify-event",   self.motion_notify_event)
        self.code_edit_text_view.connect("button-press-event",    self.button_press_event)
        self.code_edit_text_view.connect("key-press-event",       self.key_press_event)
        # input IMMulticontext event.
        self.code_edit_text_view.connect("focus-out-event", self.get_text_view_focus_out)
        self.code_edit_text_view.connect("focus-in-event",  self.get_text_view_focus_in)
        gtk.timeout_add(self.cursor_show_time, self.set_cursor_draw_bool_time)
        # gtk.timeout_add(100, self.restart_darw_border)
        
    def restart_darw_border(self):    
        self.queue_draw()
        return True
        
    def get_conten_size(self, ch):
        if ch:
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 0, 0)
            cr = cairo.Context(surface)
            context = pangocairo.CairoContext(cr)
            layout = context.create_layout()
            layout.set_font_description(pango.FontDescription("%s %s" % (self.font_type, self.font_size)))
            layout.set_text(ch)
            return layout.get_pixel_size()
        
    def test_add_buffer_text(self, connect, text):
        text_utf_8 = text.decode('utf-8')
        # text_utf_8 = text
        for ch in text_utf_8:
            table = Table()
            table.token_ch = ch
            table.token_row = self.cursor_position_row
            table.token_column = self.cursor_position_column + 1
            
            # Test 语法.
            if ch in ["邱", "海", "龙", "暴", "风"]:
                table.token_rgb = (0, 0, 0.8)
            if ch in ["深", "度"]:
                table.token_rgb = (0.8, 0, 0)
            if ch in ['L', 'i', 'n', 't']:
                table.token_rgb = (0.8, 0.8, 0.8)
                
                self.cursor_position_column += 1
            self.tables.append(table)
            self.imm_x += 12
            
        self.set_im_position()    
    
        self.queue_draw()
        
    def test_string(self):    
        pass
        

    def scrolled_window_value_changed(self, adjustment):                
        
        # print "scrolled_window_value_changed:"
        if self.ajustment_value != adjustment.get_value():
            self.expoe_bool = True
            self.ajustment_value = adjustment.get_value()
        else:    
            self.expoe_bool = False
        # gtk.timeout_add(1000, self.set_expose_bool)
        self.code_edit_text_view.queue_draw()
        
    def set_expose_bool(self):    
        self.expoe_bool = False
        return False
        # return True
    
    #####################################################
    ###########  Init code_edit_text_view ###############    
    #####################################################    
    def set_im_position(self):
        try:
            self.imm_y = self.code_font_height/2
        except:
            self.imm_y = 0
            
        self.im.set_cursor_location((self.imm_x, self.imm_y, self.imm_x, self.imm_y))
        
    def get_text_view_focus_out(self, widget, event):    
        self.im.focus_out()
        self.queue_draw()
                
    def get_text_view_focus_in(self, widget, event):    
        self.set_im_position()
        self.im.set_client_window(widget.window)
        self.im.focus_in()                
        self.queue_draw()
        
    def get_key_name(self, keyval):    
        key_unicode = gtk.gdk.keyval_to_unicode(keyval)
        
        if key_unicode == 0:
            return gtk.gdk.keyval_name(keyval)
        else:
            return str(unichr(key_unicode))
            
        
    def get_key_event_modifiers(self, key_event): 
        modifiers = [] 
        # GDK_SHIFT_MASK
        # GDK_LOCK_MASK
        # GDK_CONTROL_MASK
        
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
            
            
    def get_cli_text(self, clipboard, text, data):
        print "get_cli_text:"
        
        print len(text)
        
        text = text.decode("utf-8")
        if text[-1] == "\n":
            text = text[:-1]
            
        for ch in text:
            if ch == "\n":
                # self.Enter()
                pass
            print ch    
        
    def key_press_event(self, widget, event):                    
        print "key_press_event:"
        key_name = self.get_keyevent_name(event)
        if key_name == "Ctrl + c":
            cli = gtk.Clipboard()
            # cli.set_text("fjskdlf")
            cli.request_text(self.get_cli_text)
        # self.im.filter_keypress(event)
        # if   event.keyval == 65362:
        #     self.move_cursor("Up")
        # elif event.keyval == 65364:
        #     self.move_cursor("Down")
        # elif event.keyval == 65361:
        #     self.move_cursor("Left")
        # elif event.keyval == 65363:
        #     self.move_cursor("Right")
        # elif event.keyval == 65293:    
        #     self.current_row += 1
        #     self.cursor_position_row += 1
        #     self.queue_draw()
        # elif event.keyval == 65288: # delete code string.    
        #     temp_table = None
        #     for table in self.tables:
        #         if table.token_row == self.current_row and table.token_column == self.cursor_position_column:
        #             temp_table = table                    
        #     if temp_table:        
        #         self.cursor_position_column -= 1
        #         self.tables.remove(temp_table)
        #         self.queue_draw()
                
    def move_cursor(self, move_type):
        if move_type == "Up":
            self.cursor_position_row -= 1        
            if self.cursor_position_row < 0:
                self.cursor_position_row = 0
        elif move_type == "Down":    
            self.cursor_position_row += 1
        elif move_type == "Left":    
            self.cursor_position_column -= 1
            if self.cursor_position_column < 0:
                self.cursor_position_column = 0
        elif move_type == "Right":    
            self.cursor_position_column += 1
            
        self.get_table_token_font_size()    
        self.cursor_draw_bool        = True
        self.queue_draw()
        
    def get_table_token_font_size(self):            
        for table in self.tables:
            if table.token_width > self.code_font_width:
                self.code_font_width = table.token_width                

    def get_index_at_event(self, widget, event, row):
        '''Get index at event.'''
        rect = widget.allocation
        cr = widget.window.cairo_create()
        context = pangocairo.CairoContext(cr)
        layout = context.create_layout()
        layout.set_font_description(pango.FontDescription("%s %s" % (self.font_size, self.font_size)))
        
        # print "event.x:", event.x
        
        token_string = ""
        token_all_width = 0
        rect = self.code_edit_text_view.get_allocation()
        for table in self.tables:
            # print "row:", table.token_row
            if table.token_row == row:
                token_string += table.token_ch
                
                if rect.x + token_all_width + self.draw_row_number_width < (event.x) < rect.x + token_all_width + self.draw_row_number_width + table.token_width:
                    break
                # elif rect.x + token_all_width + self.draw_row_number_width <= (event.x) < rect.x + token_all_width + self.draw_row_number_width +2:
                #     print "************width...number"
                #     break
                else:
                    token_all_width += table.token_width
                #     print table.token_ch
                #     print token_all_width
                #     break                
        
        self.cursor_draw_all_width = token_all_width            
        
        
    def button_press_event(self, widget, event):    
        # Get row.
        
        if self.current_row:            
            row    = int(event.y / self.code_font_height)
        else:     
            row    = 0
        # print row
        # print "!!!!!!"
        self.get_index_at_event(widget, event, row)
                
        if event.x < self.draw_row_number_width:
            self.cursor_position_column = 0
            
        self.cursor_position_row = row    
        self.cursor_position_width  = 1
        self.cursor_position_height = self.code_font_height
        self.cursor_draw_bool  = True
        self.queue_draw()
        
    def draw_cursor(self, cr, cursor_x, cursor_y, cursor_w, cursor_h):
        if self.cursor_draw_bool:
            cr.set_source_rgb(1, 0, 0)
            cr.rectangle(cursor_x +  self.draw_row_number_width + (self.cursor_draw_all_width), 
                         cursor_y + self.cursor_position_row * self.code_font_height,
                         self.cursor_position_width, 
                         self.cursor_position_height)
            cr.fill()
        pass
        
    def motion_notify_event(self, widget, event):
        # code font size.       
        # self.queue_draw()
        self.expoe_bool = False
        pass
        
    def expose_code_edit_text_view(self, widget, event):   
        # print "*********************expose_code"
        cr = widget.window.cairo_create() 
        x, y, w, h = widget.allocation
                
        self.draw_row_number_width = 70
        
        # Draw background.
        self.draw_text_view_background(cr, x, y, w, h)                
        # Draw cursor.
        self.draw_cursor(cr, x, y, w, h)
        # Draw code line.
        self.draw_text_view_line(cr, x, y, w, h)
        # Draw code string font.        
        self.draw_text_view_code_string(cr, x, y, w, h)
        # Draw border.
        self.draw_text_view_border(widget, cr, x, y, self.draw_row_number_width, y + h)
        # Draw text view row number.        
        # self.draw_text_view_row_number()        
        
        return True
    
    def set_cursor_draw_bool_time(self):    
        self.cursor_draw_bool = not self.cursor_draw_bool
        self.queue_draw()
        return True
                
    
    def draw_text_view_code_string(self, cr, code_x, code_y, code_w, code_h):
        context = pangocairo.CairoContext(cr)            
        layout = context.create_layout()
        layout.set_font_description(pango.FontDescription("%s %s" % (self.font_type, self.font_size)))        
        (text_width, text_height) = layout.get_pixel_size()            
        
        save_colume_all_width = 0
        save_row           = 0
        for table in self.tables:
            layout.set_text(table.token_ch)
            self.code_font_width, self.code_font_height = layout.get_pixel_size()
            
            if save_row != table.token_row:
                save_colume_all_width = 0
                save_row              = table.token_row
                
            # Set font position.
            cr.move_to(code_x + save_colume_all_width + self.draw_row_number_width, 
                       code_y + table.token_row * self.code_font_height)
            
            save_colume_all_width += self.code_font_width
            
            # Save font size.
            table.token_width  = self.code_font_width
            table.token_height = self.code_font_height
            # Set font rgb.
            cr.set_source_rgb(*table.token_rgb)
            # Show font.
            context.update_layout(layout)
            context.show_layout(layout)
            
        # Draw current cursor show position(rectangle).
        cr.set_source_rgba(0.5, 0.5, 0.5, 0.1)   
        cr.rectangle(code_x + self.draw_row_number_width, 
                     code_y + self.cursor_position_row * self.code_font_height, 
                     code_w - self.draw_row_number_width,  self.code_font_height)
        cr.fill()
                
        
        
    # show row number of border.
    def draw_text_view_border(self, widget, cr, border_x, border_y, border_w, border_h):        
        cr.set_source_rgba(0.1, 0.1, 0.1, 1)
        # print "draw_text_view_border:"
        # print border_w 
        # print border_x
        # print self.code_edit_text_view.allocation.x 
        rect = widget.allocation
        viewport = get_match_parent(widget, ["Viewport"])
        coordinate = widget.translate_coordinates(viewport, 
                                                  rect.x, rect.y)
        # print coordinate
        if len(coordinate) == 2:            
            offset_x, offset_y = coordinate
        else:    
            offset_x, offset_y = 0, 0
            
        cr.rectangle(-offset_x, border_y,
                     border_w, border_h)
        cr.fill()   
        
        # test draw row number.
        lien_num_height = 0
        for row in range(0, self.current_row + 1):
            context = pangocairo.CairoContext(cr)            
            layout = context.create_layout()
            if row == self.cursor_position_row:
                layout.set_font_description(pango.FontDescription("%s %s" % (self.font_type, self.font_size + 4)))
            else:    
                layout.set_font_description(pango.FontDescription("%s %s" % (self.font_type, self.font_size)))
            (text_width, text_height) = layout.get_pixel_size()            
            layout.set_text(str(row + 1))
            cr.move_to(-offset_x + 10,
                       border_y + row*self.code_font_height)
            
            lien_num_height += text_height
            cr.set_source_rgb(0, 0.8, 0)
            # Show font.
            context.update_layout(layout)
            context.show_layout(layout)
            


        # self.queue_draw()
        if self.expoe_bool:    
            self.code_edit_text_view.queue_draw_area(-offset_x, border_y, self.draw_row_number_width, border_h)    
        
        
    # code background.    
    def draw_text_view_background(self, cr, bg_x, bg_y, bg_w, bg_h):    
        cr.set_source_rgba(0, 0, 0, 1)
        cr.rectangle(bg_x + self.draw_row_number_width - 1, bg_y, 
                     bg_w - self.draw_row_number_width + 1, bg_h)
        cr.fill()
        
    # code line.    
    def draw_text_view_line(self, cr, line_x, line_y, line_width, line_height):
        self.text_view_line_x_padding = 888
        line_w_padding = 1                
        cr.set_source_rgba(1, 1, 1, 0.1)
        cr.rectangle(line_x + self.text_view_line_x_padding,
                     line_y,
                     line_w_padding,
                     line_height)
        cr.fill()

        
class Table(object):        
    def __init__(self):
        self.token_ch      = ""
        self.token_rgb     = (0, 0.5, 0) # (r, g, b)
        self.token_width   = 0
        self.token_height  = 0
        self.token_row     = 0
        self.token_column  = 0
        
class Test(object):
    def __init__(self):
        self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.win.connect("destroy", gtk.main_quit)
        self.fixed = gtk.Fixed()
        self.button = gtk.Fixed()
        self.button.set_size_request(500, 500)
        self.button_scroll = gtk.ScrolledWindow(hadjustment=None)
        
        # self.button_scroll.get_vadjustment().connect("value-changed", self.value_changed)
        self.button_scroll.set_size_request(200, 200)
        self.button_scroll.set_policy(
            # gtk.POLICY_NEVER,
            # gtk.POLICY_AUTOMATIC,
            gtk.POLICY_NEVER,
            gtk.POLICY_AUTOMATIC
            )
        self.button1 = gtk.Button("fjdskl")
        self.button.put(self.button1, 0, 0)
        # self.button.put(, 10, 10)
        self.button_scroll.add_with_viewport(self.button)        
        
        self.fixed.put(self.button_scroll, 20, 20)                
        # self.win.add(self.fixed)
        
        self.code_edit1 = CodeEdit()
        self.hbox = gtk.HBox()
        self.hbox.pack_start(CodeEdit())
        self.hbox.pack_start(CodeEdit())
        self.win.add(self.hbox)
        self.win.show_all()
        
        

        
Test()        
gtk.main()
