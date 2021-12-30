import   json,redis_connection
import PySimpleGUI as sg
import Sign_Up

# Add to cart
def Add_cart(product,username = ""):
     user = redis_connection.r.get(username)
     user = json.loads(user)
     user['cart'].append(json.dumps(product))
     redis_connection.r.set(user['username'],json.dumps(user))

def show_cart(username = ""):
    layout = [
             [sg.Text("total_price"+'\n')],
             [sg.Text(key ="total_price")],
             [sg.Button('Pay',size=(15, 2)),sg.Button('Cancel',size=(15, 2))]
    ]
    window = sg.Window('Payment', layout , margins =[150,75],font=("Myriad Pro", 14) ,finalize=True, element_justification='c')

    product_names = []
    total_price = 0
    user = redis_connection.r.get(username)
    user = json.loads(user)
    cart = user['cart']
    value_order = []
    for product in cart :
        value_order.append(product)
        product = json.loads(product)
        price = product['price']
        total_price += float(price)
    window.Element('total_price').update(total_price)



    orders = user['orders']
    num_of_keys = len(orders)
    order = {}
    order[str(num_of_keys)] = value_order
    user['orders'].append(json.dumps(order))


    while True:
        event , values = window.read()

        if event == 'Pay' :
            user['cart'] = []
            redis_connection.r.set(user['username'],json.dumps(user))
            print("Ok!")
            window.close()

        elif event == sg.WIN_CLOSED or event == 'Cancel' :
            break
    return()
