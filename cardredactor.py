import tkinter as tk
from PIL import ImageGrab
from cards import get_card_image_by_query, get_card_image_random, AmbiguousCardError
from images import WebImage

# Hack to handle garbage collection
class CurrentCard:
    def __init__(self,img,name):
        self.img = img
        self.name = "".join(c for c in name if c.isalpha() or c.isdigit() or c==' ').rstrip()

def refresh_label_image(url,name):
    loaded_image = WebImage(url).get()
    cont.img = loaded_image
    cont.name = name
    canvas.itemconfigure(image_on_canvas, image=loaded_image)
    print(url)

def refresh_image_prompt():
    qstring = query.get()
    try:
        url, name = get_card_image_by_query(qstring)
        refresh_label_image(url,name)
        er_label.configure(text='')
    except AmbiguousCardError:
        er_label.configure(text='Ambiguous Search')
        print('Ambiguous Card; Refine Search')
        
def refresh_image_random():
    url, name = get_card_image_random()
    refresh_label_image(url,name)

def capture_window():
    x1 = window.winfo_rootx() + canvas.winfo_x()
    y1 = window.winfo_rooty() + canvas.winfo_y()
    x2 = x1 + canvas.winfo_width()
    y2 = y1 + canvas.winfo_height()
    takescreenshot = ImageGrab.grab().crop((x1,y1,x2,y2))
    takescreenshot.save(f"images/{cont.name}.png")

def activate_redaction(event):
    global lastx, lasty, latest_lines
    latest_lines = []
    canvas.bind('<B1-Motion>', redact)
    lastx, lasty = event.x, event.y
    lines.append(latest_lines)

def redact(event):
    global lastx, lasty, latest_lines
    x, y = event.x, event.y
    added_line = canvas.create_line((lastx, lasty, x, lasty), width=21)
    latest_lines.append(added_line)
    #  --- PIL
    lastx = x

def undo_line(event):
    global lines
    if len(lines) > 0:
        last_line = lines.pop()
        for l in last_line:
            canvas.delete(l)

def main_screen():
    # section for monkey patches
    # tk.Canvas.create_circle = _create_circle

    global lines
    lines = []
    # initialize window
    global window
    window = tk.Tk()
    window.geometry('488x720') 
    window.title('Redactification')
    window.resizable(width=False, height=False)

    queryVar = tk.StringVar()
    
    url,name = get_card_image_random()
    print(url)
    global cont
    card_image = WebImage(url).get()
    cont = CurrentCard(card_image, name)
    global canvas
    canvas = tk.Canvas(window, bg='white', height=680, width=244)
    canvas.bind('<Button-1>', activate_redaction)
    window.bind('<Control-z>', undo_line)
    global image_on_canvas
    image_on_canvas = canvas.create_image(244,340, image=card_image)
    canvas.pack(expand='yes', fill='x')
    
    bottom = tk.Frame(window)
    bottom.pack()

    global query 
    query = tk.Entry(bottom, textvariable=queryVar)
    query.grid(row=1, column=0)
    query_button = tk.Button(bottom, text='Query', command= refresh_image_prompt)
    query_button.grid(row=1, column=1)
    
    rand_button = tk.Button(bottom, text='Rand', command= refresh_image_random)
    rand_button.grid(row=1, column=2)

    save_button = tk.Button(bottom, text='Save', command= capture_window)
    save_button.grid(row=1, column=3)

    global er_label
    er_label = tk.Label(bottom, text='')
    er_label.grid(row=1, column=4)

    window.mainloop()

main_screen()