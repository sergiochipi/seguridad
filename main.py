import socket
import subprocess
import sys
from datetime import datetime
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.clock import Clock
from pathlib import Path
from kivy.properties import ListProperty
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle

global portcount
portcount = 0
global openports
openports = []
home = str(Path.home())
global whathost
whathost = ""


class Progress(Popup):
    def __init__(self, **kwargs):
        super(Progress, self).__init__(**kwargs)
        self.content = Label(text='Scanning open ports...')
        self.size_hint = (0.3, 0.3)
        self.title= 'Server Found!'

    def open_popup(self):
        self.open()
    def dismiss_popup(self, dt):
        self.dismiss()



class Layout1(BoxLayout):
    def __init__(self, **kwargs):
        super(Layout1, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = 1, 1
        self.spacing=10

        self.remotehost = Label(text='Input remote host to ckeck for open ports', pos_hint = {'center_x': 0.5}, size_hint=(.3,0.15))
        self.add_widget(self.remotehost)
        self.remotehostinput = TextInput(multiline=False, halign = 'center', pos_hint = {'center_x': 0.5}, size_hint=(0.3, 0.15) )
        self.add_widget(self.remotehostinput)

        self.startingport = Label(text='Input starting port', pos_hint = {'center_x': 0.5}, size_hint=(.3,0.15))
        self.add_widget(self.startingport)
        self.startingport = TextInput(multiline=False, halign = 'center', pos_hint = {'center_x': 0.5}, size_hint=(0.3, 0.15) )
        self.add_widget(self.startingport)

        self.endingport = Label(text='Input ending port', pos_hint = {'center_x': 0.5}, size_hint=(.3,0.15))
        self.add_widget(self.endingport)
        self.endingport = TextInput(multiline=False, halign = 'center', pos_hint = {'center_x': 0.5}, size_hint=(0.3, 0.15) )
        self.add_widget(self.endingport)

        btn1 = Button(text='Scan for open ports',pos_hint = {'center_x': 0.5},size_hint=(0.3, 0.15))
        btn1.bind(on_press=lambda x:searchports(self.remotehostinput.text, self.startingport.text, self.endingport.text))
        self.add_widget(btn1)

        btn2 = Button(text='Save console output to file',pos_hint = {'center_x': 0.5},size_hint=(0.3, 0.15))
        btn2.bind(on_press=lambda x:Layout2().savetofile())
        self.add_widget(btn2)

        with self.canvas.before:
                Color(.4, 0, .4, mode='rgb')
                self._rect = Rectangle(size=(self.height*4,1000), pos=(self.width*2, 0))

        global whathost
        whathost = self.remotehostinput.text


        def searchports(remotehost, startingport, endingport):
            try:
                global portcount
                portcount = 0
                for port in range(int(startingport),int(endingport)+1):
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    print ("Scanning port number: "+str(port))
                    result = sock.connect_ex((remotehost, port))
                    if result == 0:
                        portcount = portcount+1
                        global openports
                        openports.append("The port number "+str(port)+" is open")
                        print ("Port {}: 	 Open".format(port))
                    sock.close()


            except KeyboardInterrupt:
                print ("You pressed Ctrl+C")
                sys.exit()

            except socket.gaierror:
                print ('Hostname could not be resolved. Exiting')
                sys.exit()

            except socket.error:
                print ("Couldn't connect to server")
                sys.exit()

            except ValueError:
                print ("Dafuq are you trying to input there?")


            popup = Popup(title='Scan complete!',
            content=Label(text="The remote host has "+str(portcount)+" open ports"),
            size_hint = (0.4, 0.4))
            popup.open()
            print(openports)


class Layout2():
    def __init__(self, **kwargs):
        super(Layout2, self).__init__(**kwargs)

    cont = 0


    def savetofile(self):
        if len(openports) == 0:
            popup1 = Popup(content=Label(text="Nothing to save, no open ports / didn't scanned a target"),size_hint=(.7,.3))
            popup1.open()
        else:
            box = BoxLayout()
            box.orientation = 'vertical'
            popup = Popup(title='¿Guardar archivo?',
            content=box,
            size_hint=(0.7, 0.4))

            btn3 = Button(text='Guardar')
            btn3.size_hint = 0.4, 0.3
            btn3.pos_hint = {'center_x': .5}
            btn3.bind(on_press=lambda x:actuallysave())
            ruta = Label(text='El fichero se guardará en: '+home+'/openports.txt')



            def actuallysave():
                f = open( (home+'/openports.txt') , "a")
                f.write("Scanned a total of "+str(portcount)+" ports\n")
                for string in openports:
                    f.write(string+"\n")
                f.close()
                popup.dismiss()
            box.add_widget(ruta)
            box.add_widget(btn3)
            popup.open()



class MyApp(App):

    def build(self):
        parent = BoxLayout(orientation='vertical')
        parent.size_hint = 1, 1
        span1 = BoxLayout(orientation='vertical')
        span1.size_hint = 1, .1
        span2 = BoxLayout(orientation='vertical')
        span2.size_hint = 1, .1

        a = Layout1()


        parent.add_widget(span1)
        parent.add_widget(a)
        parent.add_widget(span2)

        return parent

if __name__ == '__main__':
    MyApp().run()
