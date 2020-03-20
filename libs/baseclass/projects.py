from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.toast import toast
from kivymd.uix.list import TwoLineAvatarIconListItem, IRightBodyTouch
from kivymd.uix.boxlayout import MDBoxLayout
from datetime import datetime
from libs.baseclass.dbedit import DBFullRead, DBTableCreate, DBDropTable, DBRead, DBCreateProjectsTable
import sqlite3 as sql


class ListItem(TwoLineAvatarIconListItem):
    
    def delete_project(self, name_proj):
        # удаляем проект
        DBDropTable(name_proj)
        # удаляем данные о проекте
        con = sql.connect('data/testRN.db')
        with con:
            cur = con.cursor()
            cur.execute(
                'DELETE FROM projects_manager WHERE '
                'project = "'+name_proj+'"'
                )
            cur.close()
        

class Container(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True


class Projects(Screen):
    """ Экран со списком проектов, после выбора чтение данных с БД и построение экрана идентичного первому """

    with open("libs/kv/projects.kv", 'r', encoding='utf-8') as projects_KV:
        Builder.load_string(projects_KV.read())

    def __init__(self, **kwargs):
        super(Projects, self).__init__(**kwargs) 

        # добавляем в скролл существющие проекты
        if 'projects_manager' in DBFullRead():
            projects_list = DBRead('projects_manager')
            for proj in projects_list:
                Item = ListItem()
                Item.text = proj[0]
                Item.secondary_text = proj[1]
                self.ids.list_projects.add_widget(Item)
        else:
            # подключиться к БД
            con = sql.connect('data/testRN.db')
            with con:
                cur = con.cursor()
                cur.execute('CREATE TABLE IF NOT EXISTS projects_manager ('
                    'project TEXT, '
                    'time_of_create TEXT)')
                cur.close()
    
    input_dialog = None
    
    def create_project_dialog(self):
        """Creates an instance of the dialog box and displays it
        on the screen for the screen Dialogs."""

        def result(text_button, instance):
            from kivymd.toast import toast
            name_proj = str(instance.text_field.text)
            # проверка строки на наличине цифр в начале имени
            simbols = []
            n_char = []
            for i in range(1040, 1104): n_char.append(i)    # русские буквы
            for i in range(65, 91): n_char.append(i)
            for i in range(97, 123): n_char.append(i)
            for i in range(48, 58): n_char.append(i)
            n_char.append(95)
            for i in n_char:
                simbols.append(chr(i))
            print(simbols)
            if name_proj[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or ' ' in name_proj:  # проверить введенные символы, чтобы не были равны по таблице символов
                toast('ОШИБКА: Имя может содержать только буквы и цифры и не может начинаться с цифры')
            else:
                # проверка на наличие проекта с таким именем
                # если в базе нет таблицы с таким именем
                if name_proj not in DBFullRead():
                    DBCreateProjectsTable(name_proj, str(datetime.now())[:-7])
                    DBTableCreate(name_proj)
                    if name_proj in DBFullRead():
                        toast('Проект "'+name_proj+'" создан')
                        Item = ListItem()
                        Item.text = name_proj
                        Item.secondary_text = str(datetime.now())[:-7]
                        self.ids.list_projects.add_widget(Item)
                    else:
                        toast('Ошибка создания проекта')
                # иначе оповещение об ошибке
                else:
                    toast('Проект с именем "'+name_proj+'" уже существует')

        if not self.input_dialog:
            from kivymd.uix.dialog import MDInputDialog

            self.input_dialog = MDInputDialog(
                title="Создать проект",
                hint_text="Введите имя нового проекта",
                size_hint=(0.8, 0.4),
                text_button_ok="Ok",
                events_callback=result,
            )

        self.input_dialog.open()