from kivy.app import App
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.uix.floatlayout import FloatLayout 

# class ButtonWidget(Button):
#     pass
Shapes_list = ["Sphere","Cube"] # change to file I/O
class InterfaceApp(App):
    def __init__(self):
        super(InterfaceApp,self).__init__()

    def build(self):
        dropdown = DropDown()
        root = FloatLayout()
        mainbutton = Button(text='Shapes', size_hint=(.1, .05),pos_hint={'x':.2, 'y':.9})
        mainbutton.bind(on_release=dropdown.open)
        for index in range(len(Shapes_list)):
            btn = Button(text=Shapes_list[index],size_hint=(None, None),height=20)
            # btn.bind(on_release= self.selection(index))
            btn.bind(on_release = lambda btn: dropdown.select(btn.text))

            dropdown.add_widget(btn)
        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x),\
            on_press=self.selection(index))
        root.add_widget(mainbutton)
        return root        

    # def build(self):
    #     dropdown = DropDown()
    #     root = FloatLayout()
    #     mainbutton = ButtonWidget()
    #     btn1 = Button(text="Sphere", size_hint_y=None, height=20)
    #     dropdown.add_widget(btn1)
    #     btn2 = Button(text="Cube", size_hint_y=None, height=20)
    #     dropdown.add_widget(btn2)

    #     mainbutton.bind(on_release=dropdown.open)
    #     dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
    #     root.add_widget(mainbutton)
    #     return root

    def selection(self,index):
        print Shapes_list[index]

if __name__ == '__main__':
    InterfaceApp().run()