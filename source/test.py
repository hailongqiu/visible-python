#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 Deepin, Inc.
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
from manage import Manage
from window import window
from button import Button

class Test(object):
    
    def __init__(self):
        self.win = window
        self.win.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.manage = Manage()
        self.win.connect("destroy", gtk.main_quit)
        self.win.connect("motion-notify-event", self.motion_get_position)
        self.win.connect("expose-event", self.draw_all_widget)
        self.button = Button(x = 30, y = 20)
        self.button2 = Button(text="dsfd", x = 10, y = 10, width=120, height=30)
        self.win.show_all()
        
    def draw_all_widget(self, widget, event):
        self.button.draw_button(widget, event)
        self.button2.draw_button(widget, event)
        return True
    
    def motion_get_position(self, widget, event):
        self.button2.x = 30
        self.button2.y = 30
        self.win.queue_draw()
        self.manage.get_position(event)
        
Test()        
gtk.main()
