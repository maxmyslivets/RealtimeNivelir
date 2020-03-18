from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivymd.toast import toast
from kivymd.uix.label import MDLabel


class Stantion_1(BoxLayout):
    """ Прямой ход """
    
    def dop_result_1(self, name_proj,
        name_stantion,
        sp, sz, 
        zo1, zo2, 
        po1, po2, 
        pd1, pd2, 
        zd1, zd2):
        print('прямой', name_proj, name_stantion,
        sp, sz, 
        zo1, zo2, 
        po1, po2, 
        pd1, pd2, 
        zd1, zd2)

        # среднее из 2х отсчетов по ЗО, ПО, ПД, ЗД
        zo = (zo1+zo2)/2
        po = (po1+po2)/2
        pd = (pd1+pd2)/2
        zd = (zd1+zd2)/2

        # разница средних по О и Д
        razn_o = max([zo, po]) - min([zo, po])
        razn_d = max([pd, zd]) - min([pd, zd])

        # входное число на допуск
        d = abs(razn_d - razn_o)
        self.ids.dop_btn.text = str(round(d / 0.014 * 100))+'%\nот\nдопуска'

        # проверка на допуск, если вошло:
        if d <= 0.0140:

            # среднее из разниц
            sr_razn = (razn_o+razn_d)/2

            # коэффициент превышения
            if zo < po:
                k_h = -1
            else:
                k_h = 1

            # превышение
            h = (sr_razn*50/1000)*k_h
            # сумма плеч
            s = sp+sz

            # обновление MDLabel h
            self.ids.h_res.text = 'h = '+str(round(h, 4))

            return True # Цвет кнопки не меняется

        else:
            # всплывающее уведомление
            toast('Значение НЕ В ДОПУСКЕ!')
            self.ids.h_res.text = 'h = '

            return False    # Цвет кнопки меняется (md_bg_color: .9, .16, .16, 1) 


class Stantion_2(BoxLayout):
    """ Обратный ход """
    
    def dop_result_2(self, name_proj,
        name_stantion,
        sp, sz, 
        zo1, zo2, 
        po1, po2, 
        pd1, pd2, 
        zd1, zd2):
        print('обратный',  name_proj, name_stantion,
        sp, sz, 
        zo1, zo2, 
        po1, po2, 
        pd1, pd2, 
        zd1, zd2)

        # среднее из 2х отсчетов по ЗО, ПО, ПД, ЗД
        zo = (zo1+zo2)/2
        po = (po1+po2)/2
        pd = (pd1+pd2)/2
        zd = (zd1+zd2)/2

        # разница средних по О и Д
        razn_o = max([zo, po]) - min([zo, po])
        razn_d = max([pd, zd]) - min([pd, zd])

        # входное число на допуск
        d = abs(razn_d - razn_o)
        self.ids.dop_btn.text = str(round(d / 0.014 * 100))+'%\nот\nдопуска'

        # проверка на допуск, если вошло:
        if d <= 0.0140:

            # среднее из разниц
            sr_razn = (razn_o+razn_d)/2

            # коэффициент превышения
            if zo < po:
                k_h = -1
            else:
                k_h = 1

            # превышение
            h = (sr_razn*50/1000)*k_h
            # сумма плеч
            s = sp+sz

            # обновление MDLabel h
            self.ids.h_res.text = 'h = '+str(round(h, 4))

            return True # Цвет кнопки не меняется

        else:
            # всплывающее уведомление
            toast('Значение НЕ В ДОПУСКЕ!')
            self.ids.h_res.text = 'h = '

            return False    # Цвет кнопки меняется (md_bg_color: .9, .16, .16, 1) 


class Obr_label(MDLabel):
    text = '  Обратный ход'
    #size_hint_y = None
    #height = "40dp"


class Create_project(Screen):
    """ Чистый экран (то, что уже готово, ток добавить обратный ход и добавить функцию удаления бокса станции) """
    
    with open("libs/kv/create_project.kv", 'r', encoding='utf-8') as create_project_KV:
        Builder.load_string(create_project_KV.read())
    
    def add_stantion_label_1(self):
        label1 = Stantion_1()
        self.ids.list1.add_widget(label1)
    
    def add_stantion_label_2(self):
        label2 = Stantion_2()
        self.ids.list2.add_widget(label2)