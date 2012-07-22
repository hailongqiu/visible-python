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


class Regex(object):
    def __init__(self, String, Format):
        self.string = String
        self.format = Format
        
    def start_regex(self):                
        print self.format
        print self.string
        
        start_index, end_index = 0,0
        return start_index, end_index
        
if __name__ == "__main__":
    start_index, end_index = Regex("I love c and linux", "i*t").start_regex()
    print "start_index:", start_index, "end_index:", end_index
    
    
    
    
    
