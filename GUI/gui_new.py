#coding=utf-8 
from kivy.app import App
from kivy.uix.button import Button
# from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown

class InterfaceApp(App):
    def __init__(self):
        super(InterfaceApp,self).__init__()
# use floatlayout for a prettier display 
    def build(self):
        layout = GridLayout(cols=1,row_force_default=True, row_default_height=30)
        label = Label(text='How many objects do you want in the scene?')#,halign="left")
        layout.add_widget(label)
        mainbutton = Button(text='Please choose', size_hint_x=None, width=300)
        Quant_Select = DropDown()
        for index in xrange(1,6):
            btn = Button(text=str(index), size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: Quant_Select.select(btn.text))
            Quant_Select.add_widget(btn)
        mainbutton.bind(on_release=Quant_Select.open)

        Quant_Select.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        layout.add_widget(mainbutton)
        btn = Button(text='OK', size_hint_x=None, width=100)#,on_press=)
        layout.add_widget(btn)
        return layout

if __name__ == '__main__':
    InterfaceApp().run()

#获取另一个widget值,用kivy language  (root.label_text)
# https://stackoverflow.com/questions/30202801/how-to-access-id-widget-of-different-class-from-a-kivy-file-kv
#显示隐藏widget内容，当判断条件为真时，再add_widget
