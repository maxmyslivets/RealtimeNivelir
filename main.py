from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivymd.toast import toast
from libs.baseclass.projects import Projects
from libs.baseclass.project_edit import Project_edit


class Home(Screen):
    """ Пустой экран, кнопка меню в правом верхнем углу:
    [создать проект, открыть проект, удалить проект, документация, экспорт, ведомость].
    Идея на миллион:
    боковое меню - [создать проект, открыть проект, документация],
    кнопка на тулбаре - [ведомость, экспорт, удалить проект]. """
    
    with open("libs/kv/home.kv", 'r', encoding='utf-8') as home_KV:
        Builder.load_string(home_KV.read())


class Documentation(Screen):
    """ Экран списка документов, при выборе - переход на экран пролистывания (если упростить, то просто открытие pdf через встроенное приложение)
 """

    with open("libs/kv/documentation.kv", 'r', encoding='utf-8') as documentation_KV:
        Builder.load_string(documentation_KV.read())

class Export(Screen):
    """ Генерация txt файлов по шаблону """

    with open("libs/kv/export.kv", 'r', encoding='utf-8') as export_KV:
        Builder.load_string(export_KV.read())


class Vedomost(Screen):
    """ Генерация doc файлов по шаблону """
    
    with open("libs/kv/vedomost.kv", 'r', encoding='utf-8') as vedomost_KV:
        Builder.load_string(vedomost_KV.read())


class RealtimeNivelirApp(MDApp):

    def build(self):

        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"

        sm = ScreenManager()
        sm.add_widget(Home(name='home'))
        sm.add_widget(Projects(name='projects'))
        sm.add_widget(Project_edit(name='project_edit'))
        sm.add_widget(Documentation(name='documentation'))
        sm.add_widget(Export(name='export'))
        sm.add_widget(Vedomost(name='vedomost'))

        return sm


if __name__ == "__main__":
    RealtimeNivelirApp().run()