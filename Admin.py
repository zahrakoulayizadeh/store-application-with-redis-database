#Enter az Admin
import   json,redis_connection
import Show_products,Sign_Up
import PySimpleGUI as sg
from documentStore import DocumentStore
from invertedIndex import InvertedIndex
from document import Document


def Admin() :

    layout = [
                [sg.Button('Add new product' , size =(15 , 2)), sg.Button('Add new user' , size =(15 , 2))],
                [sg.Text(size=(12,1), key='-TEXT-')],
                [sg.Button('Exit',size=(15,1))]
    ]


    window =sg.Window('Admin', layout , margins =[150,75],font=("Myriad Pro", 14) , element_justification='c')
    while True:
        event, values = window.read()
        if event == 'Add new product' :
            window.close()
            Add_product()

        elif event == 'Add new user' :
            window.close()
            Sign_Up.sign_up()


        # if user closes window or clicks on Exit
        elif event == sg.WIN_CLOSED or  event == 'Exit' :
            break

    window.close()
###########################################################################################################
#Add new Product:
def Add_product():
    file_types = [("JPEG (*.jpg)", "*.jpg"),
                  ("All files (*.*)", "*.*")]
    first_list_column = [
                [sg.Text("Product ID:")], [sg.In(size=(30, 8), enable_events=True)],
                [sg.Text("Product Class:")],
                [sg.Combo(['Electronics','Books','Home_Kitchen', 'Clothing','Industrial_Scientific'],
                default_value='Choose your product category.',size=(25, 8))],
                [sg.Text("Product Name:")],
                [sg.In(size=(30, 8), enable_events=True)]
                ]
    second_list_column = [
                [sg.T("Price:")],[ sg.In(size=(30,8), enable_events=True)],
                [sg.Text("Stock:")],[ sg.In(size=(30, 8), enable_events=True)],
                [sg.Text("Color:")],[sg.In(size=(30, 8), enable_events=True)],
                ]

    image_viewer_column = [ [sg.Text("product_picture:"), sg.In(size=(30, 8), enable_events=True),sg.FileBrowse(file_types=file_types)] ]
    Details_column = [[sg.Text("Product Details :")], [sg.In(size = (62,30))]]

    layout = [
                [sg.Column(first_list_column),
                sg.Column(second_list_column),
                ],
                [sg.Column(image_viewer_column)],
                [sg.Column(Details_column)],
                [sg.Button('Submit' , size =(15 , 2)), sg.Button('Cancel' , size =(15 , 2))]
    ]


    window =sg.Window('Add New Product',layout , margins =[150,75],font=("Myriad Pro", 14) , element_justification='c')

    while True:
        event, values = window.read()

        product = {

            'product_id' : values[0],
            'product_class':values[1],
            'product_Name' :values[2],
            'price':values[3],
            'tedad':values[4],
            'color':values[5],
            'product_pic':values[6],
            'product_details': values[7]
        }

        if event == 'Submit' :
            redis_connection.r.lpush('Store_products', json.dumps(product))
            redis_connection.r.set(product['product_id'], json.dumps(product))
            redis_connection.r.lpush(product['product_class'], json.dumps(product))
            redis_connection.r.bgsave()
            sg.popup('Product added successfully'+ '\n'+'\n' ,font =("Myriad Pro", 14))
            window.close()
            break



        elif event == sg.WIN_CLOSED or event == 'Cancel' :
            break

    window.close()
    # Admin()
