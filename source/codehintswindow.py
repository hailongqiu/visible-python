


import gtk

class CodeHintsWindow(gtk.Window):
    def __init__(self, width=100, height=100):
        gtk.Window.__init__(self)
        # alignment.
        self.win_ali = gtk.Alignment()
        # set window size.
        self.set_size_request(width, height)
        # Set window type.
        self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_COMBO)
        # Taskbar hide taskbar.
        self.set_skip_taskbar_hint(True)
        # Set window keep above.
        self.set_keep_above(True)        
        
        # Scrolledwindow init.
        self.scrol_win = gtk.ScrolledWindow()
        self.scrol_win.set_policy(
            gtk.POLICY_AUTOMATIC,
            # gtk.POLICY_AUTOMATIC
            gtk.POLICY_ALWAYS
            )
        
        # strings show.
        self.show_text_list = gtk.Button()
        self.scrol_win.add_with_viewport(self.show_text_list)

        self.win_ali.set(1, 1, 1, 1)
        self.win_ali.set_padding(2, 2, 2, 2)
        self.win_ali.add(self.scrol_win)
        self.add(self.win_ali)
        
        # Init window connect.
        self.connect("expose-event", self.window_expose_event)
        # Init text list connect.
        self.show_text_list.connect("expose-event", self.show_text_list_expose_event)
                
    def move_window(self, x, y):
        self.move(x, y)
        
    def show_text_list_expose_event(self, widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation                        
        cr.set_source_rgb(1, 1, 1)
        cr.rectangle(
            rect.x, 
            rect.y,
            rect.width,
            rect.height
            )
        cr.fill()                
        return True
    
    def window_expose_event(self, widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation
        
        # draw window background.
        self.draw_window_background(cr, rect)
        #         
        
        if "get_child" in dir(widget) and widget.get_child() != None:
            widget.propagate_expose(widget.get_child(), event)
            
        return True
        
    def draw_window_background(self, cr, rect):        
        cr.set_source_rgb(1, 1, 1)
        cr.rectangle(
            rect.x, 
            rect.y,
            rect.width,
            rect.height
            )
        cr.fill()        
        cr.set_source_rgb(0, 0, 0)
        cr.rectangle(
            rect.x, 
            rect.y,
            rect.width,
            rect.height
            )
        cr.stroke()         
        cr.set_source_rgba(*self.color_to_rgba("#A9A9A9", 0.7))
        cr.rectangle(
            rect.x + 1, 
            rect.y + 1,
            rect.width - 2,
            rect.height - 2
            )
        cr.stroke() 
        
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
        
    
