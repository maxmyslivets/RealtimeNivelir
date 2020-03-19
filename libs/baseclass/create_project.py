from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivymd.toast import toast
from kivymd.uix.label import MDLabel
from libs.baseclass.dbedit import *


class Stantion_1(BoxLayout):
    """ Прямой ход """

    def dop_result_1(self,
        name_stantion,
        sp, sz, 
        zo1, zo2, 
        po1, po2, 
        pd1, pd2, 
        zd1, zd2):

        name_proj = self.id
        type_po = 'Прямой ход'

        # среднее из 2х отсчетов по ЗО, ПО, ПД, ЗД
        zo = round(((zo1+zo2)/2), 5)
        po = round(((po1+po2)/2), 5)
        pd = round(((pd1+pd2)/2), 5)
        zd = round(((zd1+zd2)/2), 5)

        # разница средних по О и Д
        razn_o = round((max([zo, po]) - min([zo, po])), 5)
        razn_d = round((max([pd, zd]) - min([pd, zd])), 5)

        # входное число на допуск
        d = round(abs(razn_d - razn_o), 4)
        d_res = str(round(d / 0.014 * 100))+'%'
        self.ids.dop_btn.text = str(round(d / 0.014 * 100))+'%\nот\nдопуска'

        # среднее из разниц
        sr_razn = round(((razn_o+razn_d)/2), 5)

        # коэффициент превышения
        if zo < po:
            k_h = -1
        else:
            k_h = 1

        # превышение
        h = round(((sr_razn*50/1000)*k_h), 4)
        # сумма плеч
        s = sp+sz

        # обновление MDLabel h
        self.ids.h_res.text = 'h = '+str(round(h, 4))
        
        # проверка, если не вошло в допуск:
        if d > 0.0140:
            toast('Значение НЕ В ДОПУСКЕ!')
            self.ids.h_res.text = 'h = '
            return False # Цвет кнопки меняется
        
        # Добавление данных в БД
        row = [name_proj, type_po, name_stantion, sp, sz, zo1, zo2, po1, po2, pd1, pd2, zd1, zd2, zo, po, pd, zd, razn_o, razn_d, d, d_res, sr_razn, k_h, h, s]
        
        if len(DBFullRead()) == 0:
            DBAdd(row)
        elif name_proj not in DBFullRead():
            print('В базе нет таблицы', name_proj, ', добавляем таблицу и строку')
            # добавить строку в таблицу
            DBAdd(row)
        else:
            print('В базе есть такая таблица')
            # если в таблице есть такая строка
            if DBTestCastom(row):
                print('В таблице есть такая строка\nУдаляем строку')
                # удалить строку
                DBDelete(row)
                print('Добавляем строку')
                # добавить строку
                DBAdd(row)
            # иначе добавляем строку
            else:
                print('В таблице нет такой строки\nДобавляем строку')
                DBAdd(row)
        
        return True # Цвет кнопки не меняется (md_bg_color: .9, .16, .16, 1)


class Stantion_2(BoxLayout):
    """ Обратный ход """
    
    def dop_result_2(self,
        name_stantion,
        sp, sz, 
        zo1, zo2, 
        po1, po2, 
        pd1, pd2, 
        zd1, zd2):

        name_proj = self.id
        type_po = 'Обратный ход'

        # среднее из 2х отсчетов по ЗО, ПО, ПД, ЗД
        zo = round(((zo1+zo2)/2), 5)
        po = round(((po1+po2)/2), 5)
        pd = round(((pd1+pd2)/2), 5)
        zd = round(((zd1+zd2)/2), 5)

        # разница средних по О и Д
        razn_o = round((max([zo, po]) - min([zo, po])), 5)
        razn_d = round((max([pd, zd]) - min([pd, zd])), 5)

        # входное число на допуск
        d = round(abs(razn_d - razn_o), 4)
        d_res = str(round(d / 0.014 * 100))+'%'
        self.ids.dop_btn.text = str(round(d / 0.014 * 100))+'%\nот\nдопуска'

        # среднее из разниц
        sr_razn = round(((razn_o+razn_d)/2), 5)

        # коэффициент превышения
        if zo < po:
            k_h = -1
        else:
            k_h = 1

        # превышение
        h = round(((sr_razn*50/1000)*k_h), 4)
        # сумма плеч
        s = sp+sz

        # обновление MDLabel h
        self.ids.h_res.text = 'h = '+str(round(h, 4))
        
        # проверка, если не вошло в допуск:
        if d > 0.0140:
            toast('Значение НЕ В ДОПУСКЕ!')
            self.ids.h_res.text = 'h = '
            return False # Цвет кнопки меняется
        
        # Добавление данных в БД
        row = [name_proj, type_po, name_stantion, sp, sz, zo1, zo2, po1, po2, pd1, pd2, zd1, zd2, zo, po, pd, zd, razn_o, razn_d, d, d_res, sr_razn, k_h, h, s]
        
        if len(DBFullRead()) == 0:
            DBAdd(row)
        elif name_proj not in DBFullRead()[0]:
            print('В базе нет таблицы, добавляем таблицу и строку')
            # добавить строку в таблицу
            DBAdd(row)
        else:
            print('В базе есть такая таблица')
            # если в таблице есть такая строка
            if DBTestCastom(row):
                print('В таблице есть такая строка\nУдаляем строку')
                # удалить строку
                DBDelete(row)
                print('Добавляем строку')
                # добавить строку
                DBAdd(row)
            # иначе добавляем строку
            else:
                print('В таблице нет такой строки\nДобавляем строку')
                DBAdd(row)
        
        return True # Цвет кнопки меняется (md_bg_color: .9, .16, .16, 1)


class Obr_label(MDLabel):
    text = '  Обратный ход'
    #size_hint_y = None
    #height = "40dp"


class Create_project(Screen):
    """ Чистый экран (то, что уже готово, ток добавить обратный ход и добавить функцию удаления бокса станции) """
    
    with open("libs/kv/create_project.kv", 'r', encoding='utf-8') as create_project_KV:
        Builder.load_string(create_project_KV.read())
    
    def add_stantion_label_1(self, name_proj):
        label1 = Stantion_1()
        label1.id = name_proj
        self.ids.list1.add_widget(label1)

    def add_stantion_label_2(self, name_proj):
        label2 = Stantion_2()
        label2.id = name_proj
        self.ids.list2.add_widget(label2)