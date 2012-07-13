


import gtk

class Test(object):
    def __init__(self):
        self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.win.connect("destroy", gtk.main_quit)
        self.fixed = gtk.Fixed()
        self.button = gtk.Fixed()
        self.button.set_size_request(200, 200)
        self.button_scroll = gtk.ScrolledWindow(hadjustment=None)
        self.button_scroll.set_size_request(200, 200)
        self.button_scroll.set_policy(
            # gtk.POLICY_NEVER,
            # gtk.POLICY_AUTOMATIC,
            gtk.POLICY_NEVER,
            gtk.POLICY_AUTOMATIC
            )
        self.button.put(gtk.Button("fjdskl"), 10, 180)
        
        self.button_scroll.add_with_viewport(self.button)        
        
        self.fixed.put(self.button_scroll, 20, 20)                
        self.win.add(self.fixed)
        self.win.show_all()
        
Test()        
gtk.main()
