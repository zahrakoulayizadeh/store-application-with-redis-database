import   json,redis_connection
import PySimpleGUI as sg
import Show_products , Search , My_Cart


def sign_up():
    first_list_column = [  [sg.Text("Username:")], [sg.In(size=(30, 5), enable_events=True)],
                            [sg.Text(size=(12,1), key='-TEXT-')],
                [sg.Text("First_name:")], [sg.In(size=(30, 5), enable_events=True)],
                [sg.Text(size=(12,1), key='-TEXT-')],
                [sg.Text("Last_name:")], [sg.In(size=(30, 5), enable_events=True)]
                ]
    second_list_column = [
                [sg.T("Password:")],[ sg.In(size=(30, 5), enable_events=True)],
                [sg.Text(size=(12,1), key='-TEXT-')],
                [sg.Text("email:")],[ sg.In(size=(30, 5), enable_events=True)],
                [sg.Text(size=(12,1), key='-TEXT-')],
                [sg.Text("Phone Number:")],[sg.In(size=(30, 5), enable_events=True)]
                ]

    image_viewer_column = [ [sg.Text("profile_picture:"), sg.In(size=(30, 5), enable_events=True),sg.FileBrowse()] ]

    layout = [
                [sg.Column(first_list_column),
                sg.Column(second_list_column),
                ],
                [sg.Column(image_viewer_column)],
                [sg.Button('Submit' , size =(15 , 2)), sg.Button('Exit' , size =(15 , 2))]
    ]


    window =sg.Window('sign-up', layout , margins =[150,75],font=("Myriad Pro", 14) , element_justification='c')
    Usernames = [redis_connection.r.keys()]

    while True:
        event, values = window.read()

        profile = {

            'username' : values[0],
            'first_name':values[1],
            'last_name':values[2],
            'password':values[3],
            'email':values[4],
            'phone':values[5],
            'profile_pic':values[6],
            'cart':[],
            'orders' :[]
        }

        if event == 'Submit' :
            redis_connection.r.set(profile['username'], json.dumps(profile))
            redis_connection.r.bgsave()
            window.close()
            Menu(profile['username'])

            break

        elif event == sg.WIN_CLOSED or event == 'Exit' :
            break

    window.close()

###########################################################################################################
##Menu
def Menu(username =""):

    layout = [
                [sg.Text("Please select one of the options below",font =("Myriad Pro",16))],
                [sg.Button('Show Products',size=(30,2))],
                [sg.Text(size=(12,1), key='-TEXT-')],
                [sg.Button('Search Product',size=(30,2))],
                [sg.Text(size=(12,1), key='-TEXT-')],
                [sg.Button('Orders',size=(30,2))],
                [sg.Text(size=(12,1), key='-TEXT-')],
                [sg.Button('My Cart',size=(30,2))],
                [sg.Text(size=(12,1), key='-TEXT-')],
                [sg.Button('Exit',size=(20,1))]
    ]
    window =sg.Window('Menu', layout , margins =[150,75],font=("Myriad Pro", 14) , element_justification='c')

    while True:
        event, values = window.read()
        user = redis_connection.r.get(username)
        user = json.loads(user)
        orders = user['orders']
        cart = user['cart']

        if event == 'Show Products' :
            window.close()
            Show_products.show_products(username)

        elif event == 'Search Product' :
            window.close()
            Search.search_results(username)

        elif event == 'Orders' :
            layout = [[sg.Text("Your Orders are :",font =("Myriad Pro",14))],
                         [sg.Listbox(values=orders,
                                                     size=(70,10), change_submits=True,
                                                     bind_return_key=True,auto_size_text=True, key='_ORDERS_LISTBOX_', enable_events=True,horizontal_scroll=True)]]
            win =   sg.Window('Orders', layout ,font=("Myriad Pro", 14) , element_justification='c')
            win.read()


        elif event == 'My Cart' :
            layout = [[sg.Text("Your Cart :",font =("Myriad Pro",14))],
                         [sg.Listbox(values=cart,
                                                     size=(70,10), change_submits=True,
                                                     bind_return_key=True,auto_size_text=True, key='_ORDERS_LISTBOX_', enable_events=True,horizontal_scroll=True)]]
            win =   sg.Window('Cart', layout ,font=("Myriad Pro", 14) , element_justification='c')
            win.read()

        # if user closes window or clicks on Exit
        elif event == sg.WIN_CLOSED or  event == 'Exit':
            break

    window.close()
