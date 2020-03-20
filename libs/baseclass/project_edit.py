from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivymd.toast import toast


class Project_edit(Screen):
    """ Экран создания проекта """
    
    with open("libs/kv/project_edit.kv", 'r', encoding='utf-8') as project_edit_KV:
        Builder.load_string(project_edit_KV.read())