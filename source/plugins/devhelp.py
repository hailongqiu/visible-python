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

def devhelp(fanter_self):
    keyword = "Window"
    fanter_self.text_source_view.connect("key-press-event",  key_press_event, fanter_self, keyword)
    
def key_press_event(widget, event, fanter_self, keyword):
    key_name = fanter_self.get_keyevent_name(event)
    if key_name == "F2":
        os.system("devhelp -s %s"%(keyword))
        
    
    
    


    
    
    
    
    
    
    
