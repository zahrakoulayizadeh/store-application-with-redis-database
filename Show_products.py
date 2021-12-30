import   json,redis_connection
import PySimpleGUI as sg
import io
import os
from PIL import Image
import Sign_Up
import My_Cart


def show_products(username =""):

    dict ={''}
    layout = [
                [sg.Text("Please choose your product class:",font =("Myriad Pro",16))],
                [sg.Button('Electronics',size=(30,2))],
                [sg.Text(size=(12,1), key='-TEXT-')],
                [sg.Button('Books',size=(30,2))],
                [sg.Text(size=(12,1), key='-TEXT-')],
                [sg.Button('Home_Kitchen',size=(30,2))],
                [sg.Text(size=(12,1), key='-TEXT-')],
                [sg.Button('Clothing',size=(30,2))],
                [sg.Text(size=(12,1), key='-TEXT-')],
                [sg.Button('Industrial_Scientific',size=(30,2))],
                [sg.Text(size=(12,1), key='-TEXT-')],
                [sg.Button('Back',size=(20,1))],
                [sg.Button('Exit',size=(20,1))]
    ]
    window =sg.Window('Show Products', layout , margins =[150,75],font=("Myriad Pro", 14) , element_justification='c')
#################################################################################################################

    while True:
        event, values = window.read()

        if event == 'Electronics' :
            l = redis_connection.r.lrange('Electronics',0,-1)
            update(l,"Electronics",username)


        elif event == 'Books' :

            l = redis_connection.r.lrange('Books',0,-1)
            update(l,"Books",username)

        elif event == 'Home_Kitchen' :

            l = redis_connection.r.lrange('Home_Kitchen',0,-1)
            update(l,"Hom & Kitchen",username)

        elif event == 'Clothing' :

            l = redis_connection.r.lrange('Clothing',0,-1)
            update(l,"Clothing",username)

        elif event == 'Industrial_Scientific' :

            l = redis_connection.r.lrange('Industrial_Scientific',0,-1)
            update(l,"Industrial_Scientific",username)

        elif event == 'Back' :
            window.close()
            Sign_Up.Menu()
        # if user closes window or clicks on Exit
        elif event == sg.WIN_CLOSED or  event == 'Exit':
            break

    window.close()

#####################################################################################
#result window1
def update(list, string ,username = ""):

    column1 = [
                [sg.Text(),],
                ]

    for i in range(len(list)):
        column1.append([sg.Text('\n'+"Image"+'\n')])
        column1.append([sg.Text("*"*20)])
        column1.append([sg.Text(text_color='yellow',key = str(i))])
        column1.append([sg.Button('Add to Cart',key =str(i))])
        column1.append([sg.Text("*"*100)])




    layout = [

                [sg.Column(column1,scrollable = True , size = (800,600))

                ],
                [sg.Button('Cart' , size =(15 , 2)), sg.Button('Cancel' , size =(15 , 2))]

    ]
    window1 =sg.Window(string, layout,font=("Myriad Pro", 12),finalize=True , element_justification='l',resizable = True)

    for i in range(len(list)):
        dict = json.loads(list[i])
        stock = str(dict['tedad'])
        str1 = "product_ID:    "+str(dict['product_id']) +"          "+"product_Name:    "+ str(dict['product_Name'])+ '\n'
        str2 = "Price:    " + str(dict['price'])+ "$" +"          "+ "Color:    " + str(dict['color']) +"          "+"Stock:    " + stock + '\n'
        str3 = "More Datails:    " + str(dict['product_details'])
        s = str1 + str2 + str3
        window1.Element(str(i)).update(s)
    while True:
        event, values = window1.read()

        for i in range(len(list)):

            if event == str(i)+str(i) :
                dict = json.loads(list[i])
                My_Cart.Add_cart(dict,username)
                sg.popup('Add','The product added to you cart :', str(dict['product_id']))


        if event == 'Cart' :
            window1.close()
            My_Cart.show_cart(username)

        # if user closes window or clicks on Exit
        if event == sg.WIN_CLOSED or event == 'Cancel' :
            break

    window1.close()
