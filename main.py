import PySimpleGUI as sg
import Sign_Up
import Admin

def main() :

    sg.theme('DarkGreen4')
    layout = [  [sg.Text("Welcome to Zahra's  Store!",font =("Myriad Pro",16))],
                [
                sg.Button('Enter as Admin',size=(15,2))],
                [sg.Text(" "*30)],
                [sg.Text('New costumer?',font =("Myriad Pro",16))],
                 [sg.Button('Sign_Up here!',size=(15,2))],
                [sg.Button('Exit',size=(15,1))]
                ]


    window = sg.Window('Welcome', layout , margins =[150,75],font=("Myriad Pro", 14) , element_justification='c')

    while True:
        event, values = window.read()

        if event == 'Sign_Up here!' :            
            Sign_Up.sign_up()

        elif event == 'Enter as Admin' :
            Admin.Admin()

        # if user closes window or clicks on Exit
        elif event == sg.WIN_CLOSED or  event == 'Exit':
            break

    window.close()
main()
