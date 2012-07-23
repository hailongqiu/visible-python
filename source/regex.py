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

from ini import Config

SYMBOL_TABLE_KEYWORD_TYPE   = 0 # 关键字
SYMBOL_TABLE_FUNCTION_TYPE  = 1 # 函数名
SYMBOL_TABLE_CLASS_TYPE     = 2 # 类名
SYMBOL_TABLE_STRING_TYPE    = 3 # 字符串
SYMBOL_TABLE_VARIABLE_TYPE  = 4 # 变量
SYMBOL_TABLE_SYMBOL_TYPE    = 5 # 符号
SYMBOL_TABLE_NUMBER_TYPE    = 6 # 数字

class SymbolTable(object):
    def __init__(self):
        self.type = 0
        self.token = ""
        self.start_index = 0
        self.end_index   = 0
        self.row         = 0
        self.rgb         = "#000000"
        
class Scan(object):        
    def __init__(self, language_file):
        self.symbol_table_list = []
        self.symbol = ["~", "`", "!", "@", "#", 
                       "$", "%", "^", "&", "*",                        
                       "(", ")", "+", "-", 
                       "=", "[", "{", "}", "]", 
                       "|", "\\", ":", ";", "'", 
                       "<", ",", ">", ".", "/", "?"]        
        
        self.config = Config(language_file)
        self.keyword = self.config.get_argvs("keyword").keys()
        ##########Index.###########################
        self.index = 0
        self.start_index = 0
        self.end_index = 0
        self.row  = None
        ###########save text and token.############
        self.text  = ""
        self.token = ""
        self.type  = 4
        
        self.class_type = "class"
        self.function_type = "def"
        self.variable_type = "self"
        
    def scan(self, text, row):    
        self.text = text
        self.row  = row
        while True:
            ch = self.text[self.index]
            if ch not in [" "]:
                if ('a' <= ch <= 'z') or ('A' <= ch <= 'Z'):
                    self.type_bool(ch)                    
                elif '0' <= ch <= '9':    
                    self.start_index = self.index
                    self.number_bool(ch)
                elif ch in self.symbol:
                    print "符号处理:...", ch
                    print "start_index:", self.index
                    print "end_index:", self.index
                    self.index += 1            
            else:
                self.index += 1
                
            if self.index == (len(text)):
                break
            
        ########################################
        ## return symbol table list.    
        return self.symbol_table_list
    
    ################################################################        
    ### number bool.        
    def number_bool(self, ch): 
        self.token = ""
        while True:
            if not '0' <= self.text[self.index] <= '9' and self.text[self.index] != " ":
                self.index = self.start_index + 1
                self.variable_bool(self.text[self.index - 1])
                break
            
            if self.text[self.index] == " ":
                symbol_table = SymbolTable()
                symbol_table.type  = SYMBOL_TABLE_NUMBER_TYPE
                symbol_table.token = self.token
                symbol_table.row   = self.row
                symbol_table.start_index = self.start_index
                symbol_table.end_index   = self.end_index                
                # symbol_table.rgb = 
                ############################################
                print "数字:==============================="
                print "type:", symbol_table.type
                print "token:", symbol_table.token
                print "row:", symbol_table.row
                print "start_index:", symbol_table.start_index
                print "end_index:", symbol_table.end_index
                print "=============================="
                ############################################
                self.symbol_table_list.append(symbol_table)
                break
            else:
                self.token += self.text[self.index]
                
            self.index += 1
            
    ################################################################        
    ### keyword bool and variable name(class name or function name or variable name)  
    def type_bool(self, ch): 
        if self.keyword_bool(ch): # 
            symbol_table = SymbolTable()
            symbol_table.type  = SYMBOL_TABLE_KEYWORD_TYPE
            symbol_table.token = self.token
            symbol_table.row   = self.row
            symbol_table.start_index = self.start_index
            symbol_table.end_index   = self.end_index
            symbol_table.rgb         = self.config.get("keyword", str(self.token))
            ################################################
            print "关键字:=================================="
            print "type:", symbol_table.type
            print "token:", symbol_table.token
            print "row:", symbol_table.row
            print "start_index:", symbol_table.start_index
            print "end_index:", symbol_table.end_index
            print "rgb:", symbol_table.rgb
            print "========================================"
            ################################################
            self.symbol_table_list.append(symbol_table)
            # Set type.
            if self.token == self.class_type:
                self.type = SYMBOL_TABLE_CLASS_TYPE
            elif self.token == self.function_type:    
                self.type = SYMBOL_TABLE_FUNCTION_TYPE
            elif self.token == self.variable_type:    
                self.type = SYMBOL_TABLE_VARIABLE_TYPE
        else:    
            self.variable_bool(ch)
            
    def variable_bool(self, ch):
        self.token = ""
        self.token += ch
        self.start_index = self.index
        while True:                
            if (self.text[self.index] in [" "]) or (self.text[self.index] in self.symbol):
                self.end_index = self.index
                symbol_table = SymbolTable()
                symbol_table.type  = self.type
                symbol_table.token = self.token
                symbol_table.row   = self.row
                symbol_table.start_index = self.start_index - 1
                symbol_table.end_index   = self.end_index - 1
                # class name or function name or VARIABLE_TYPE.
                # symbol_table.rgb         = self.config.get("keyword", str())
                self.symbol_table_list.append(symbol_table)                
                #############################################
                print "常量:================================="
                print "type:", symbol_table.type
                print "token:", symbol_table.token
                print "row:", symbol_table.row
                print "start_index:", symbol_table.start_index
                print "end_index:", symbol_table.end_index
                print "rgb:还未设定..."
                print "======================================"
                #############################################
                break                                                

            self.token += self.text[self.index]
            self.index += 1

    def keyword_bool(self, ch):
        for key in self.keyword:
            if key[0] == ch:
                self.start_index = self.index # Save start index.
                if self.keyword_bool_scan(key):
                    return True                
                
        self.index += 1
                
    def keyword_bool_scan(self, key):            
        self.token = ""
        for k in key:
            if k == self.text[self.index]:
                self.token += self.text[self.index]
                self.index += 1                             
                
        if (self.index == self.start_index + len(key) and 
                (self.text[self.index] in [" "] or self.text[self.index] in self.symbol)):
            self.end_index = self.index - 1
            return True
        else:
            self.index = self.start_index
            return False
                
scan = Scan("language/python.ini")
scan.scan("raw_input_123456 is name = 3454_abc_34 5678 class import def function(self, a, b\\)", 10)
##########################################################################

##########################################################################

class Regex(object):
    def __init__(self, String, Format):
        self.string = String
        self.format = Format
        
    def start_regex(self):                
        print self.format
        print self.string
                
        self.token_bool(self.format[0])                
        start_index, end_index = 0,0
        return start_index, end_index
    
    def token_bool(self, token):                    
        if   token == "-":
            pass
        elif token == "*":   
            pass
        elif token == "":
            pass
        
        return token    
    
class Stack(object):
    def __init__(self):
        self.__stack = []
        self.__index = -1
    
    def pop(self):
        if self.__index > -1:
            element = self.__stack[self.__index]
            del self.__stack[self.__index]
            self.__index -= 1
            return element 
        else:
            return False
        
    def push(self, element):
        self.__stack.append(element)
        self.__index += 1
    
# if __name__ == "__main__":
#     # start_index, end_index = Regex("I love c and linux", "0-9").start_regex()
#     # print "start_index:", start_index, "end_index:", end_index
#     temp_stack = Stack()
#     temp_stack.push('a')
#     temp_stack.push('b')
#     temp_stack.push('c')
#     print temp_stack.pop()
#     print temp_stack.pop()
#     print temp_stack.pop()
    
    
    
    
