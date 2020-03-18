from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivymd.toast import toast


class Stantion(BoxLayout):
    
    def dop_result(self,
        name_stantion,
        sp, sz, 
        zo1, zo2, 
        po1, po2, 
        pd1, pd2, 
        zd1, zd2):

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

            # обновление MDLabel h и H
            self.ids.h_res.text = 'h = '+str(round(h, 4))
            #self.ids.H_res.text = 'h = '+str(round(H, 4))

            return True # Цвет кнопки не меняется

        else:
            # всплывающее уведомление
            #self.ids.dop_btn.md_bg_color = [.9, .16, .16, 1]
            toast('Значение НЕ В ДОПУСКЕ!')
            self.ids.h_res.text = 'h = '

            return False    # Цвет (md_bg_color: .9, .16, .16, 1) кнопки меняется


class II_klass(Screen):
    
    with open("kv/II_klass.kv", 'r', encoding='utf-8') as II_klass_KV:
        Builder.load_string(II_klass_KV.read())
    
    def add_stantion_label(self):
        label1 = Stantion()
        self.ids.list.add_widget(label1)


class RealtimeNivelirApp(MDApp):

    def build(self):

        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"

        sm = ScreenManager()
        sm.add_widget(II_klass(name='II_klass'))

        return sm


if __name__ == "__main__":
    RealtimeNivelirApp().run()