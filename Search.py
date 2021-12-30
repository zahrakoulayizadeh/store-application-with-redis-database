import PySimpleGUI as sg
import Sign_Up
import redis_connection,json
from documentStore import DocumentStore
from invertedIndex import InvertedIndex
from document import Document



def add_to_inverted_index(product):

    body = product['product_id'].lower() + " "
    body += product['product_class'].lower() + " "
    body += product['product_Name'].lower() + " "
    body += product['color'].lower() + " "
    body += product['tedad'].lower() + " "
    body += product['price'].lower() + " "
    body += product['product_details'].lower() + " "

    document = Document(product['product_Name'], body, product['product_id'])
    docStore.add(document)
    index.add(document)

docStore = DocumentStore()
index = InvertedIndex()
store_products = redis_connection.r.lrange("Store_products",0,-1)


for product_str in store_products:
    product = json.loads(product_str)
    add_to_inverted_index(product)


def search_results(username) :

    search_result = []

    layout = [  [sg.Text("Enter your search terms below",font =("Myriad Pro",14))],
                [
                 [sg.In(size=(50, 10), enable_events=True),sg.Button('Search',size=(10,1))]],
                 [sg.Listbox(values=[],
                                             size=(120,15),
                                             change_submits=True,
                                             bind_return_key=True,
                                             auto_size_text=True,
                                             key='_SEARCH_LISTBOX_', enable_events=True,horizontal_scroll=True)],

                [sg.Button('Exit',size=(15,1)),sg.Button('Clear',size=(15,1)),sg.Button('Back',size=(15,1))]
                ]


    window = sg.Window('Search', layout , margins =[0,0],font=("Myriad Pro", 12) , element_justification='l',finalize=True)


    while True:
        event, values = window.read()

        if event == 'Search' :
            inp = values[0].lower()
            lst = index.getPostingList(inp)
            if lst != None:
                for docId in lst.getDocIds():
                    search_result.append(redis_connection.r.get(docId))
            else:
                search_result=["No match found."]

            window.Element('_SEARCH_LISTBOX_').update(search_result)
            search_result = []


        if event == 'Clear' :
            window.Element('_SEARCH_LISTBOX_').update([])
            search_result = []
            print("Ok!")

        elif event == 'Back' :
            window.close()
            Sign_Up.Menu(username)

        # if user closes window or clicks on Exit
        elif event == sg.WIN_CLOSED or  event == 'Exit':

            break

    window.close()
