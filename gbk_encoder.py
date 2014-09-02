#coding: utf8

import sublime, sublime_plugin
import os, re

def convertEncoding(view, file_name, from_encoding, to_encoding):
    if not file_name:
        file_name = view.file_name()
    reg_all = sublime.Region(0, view.size())
    file_name = view.file_name()
    gbk = file(file_name).read()
    text = gbk.decode(from_encoding).encode(to_encoding)
    gbk = file(file_name, 'w')
    gbk.write(text)
    gbk.close()
    window = sublime.active_window()
    window.run_command('close')
    tmp_view = window.open_file(file_name)
    tmp_view.set_syntax_file(view.settings().get('syntax'))    
    window.focus_view(tmp_view)

class EventListener(sublime_plugin.EventListener):
    def on_load(self, view):
        try:
            reg_all = sublime.Region(0, view.size())
            gbk = view.substr(reg_all).encode('gbk')
        except:
            view.run_command("encodewithgbk")
            sublime.status_message('GBK encoding detected, open with UTF8 automatically.')
        return

	def on_pre_save(self, view):
	    return
	    
    def on_post_save(self, view):
        return 

    def on_close(self,view):
        return

class EncodewithgbkCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        self.view = view
    def run(self, edit):
        view = self.view
        reg_all = sublime.Region(0, view.size())
        try:
            gbk = view.substr(reg_all).encode('gbk')
        except:
            gbk = file(view.file_name()).read()
            text = gbk.decode('gbk')
            view.replace(edit, reg_all, text)

class Converttoutf8fromgbkCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        self.view = view
    def run(self, edit):
        view = self.view
        convertEncoding(view,view.file_name(),'gbk','utf8')
        sublime.status_message('The '+view.file_name()+' on disk is converted to UTF8.')

class Converttogbkfromutf8Command(sublime_plugin.TextCommand):
    def __init__(self, view):
        self.view = view
    def run(self, edit):
        view = self.view
        convertEncoding(view,view.file_name(),'utf8','gbk')
        sublime.status_message('The '+view.file_name()+' on disk is converted to GBK, and its reload with UTF8 automatically.')