import logging
from tkinter import *
from tkinter import messagebox
from db import Database
from tkinter import ttk

db = Database('store1.db')

app = Tk()

# Parts list

Columns = ('col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7')
column_name = ('id', 'part', 'customer-name', 'retailer', 'price', 'quantity', 'total-amount')
part_table = ttk.Treeview(app, columns=Columns)

# setup
part_table.column('#0', width=0, stretch=NO) 
for column in Columns:
    part_table.column(column, anchor=CENTER, width=120)
part_table.grid(row=3, column=0, columnspan=4, rowspan=6, pady=20, padx=20)



for column, heading_text in zip(Columns, column_name):
    part_table.heading(column, text=heading_text, anchor=CENTER)
    
#display all rows
def populate():
    if db is None or part_table is None:
        return

    part_table.delete(*part_table.get_children())

    try:
        data = db.fetch()
    except Exception as e:
        logging.error(str(e))
        return

    if data:
        for row in data:
            row1 = list(row)
            row1.append(row[-1] * row[-2])
            part_table.insert(parent='', index='end', id=row[0], text='', values=row1)

#add items to  table
def additem():
    if part_text.get() == '' or customer_text.get() == '' or retailer_text.get() == '' or price_text.get() == '' or quantity_text.get() == '':
        messagebox.showerror("Required field", "Please include all fields")
    else:
        db.insert(part_text.get(), customer_text.get(), retailer_text.get(), price_text.get(), quantity_text.get())
        populate()

#select particular item
def select_item(event):
    global selected_item
    Selected_items = part_table.selection()
   
    if Selected_items:
        index = Selected_items[0]
        selected_item = part_table.item(index)
      
    else:
        print("No item selected")
    part_input.delete(0,END)
    part_input.insert(END,selected_item['values'][1])
    customer_input.delete(0,END)
    customer_input.insert(END,selected_item['values'][2])
    retailer_input.delete(0,END)
    retailer_input.insert(END,selected_item['values'][3])
    price_input.delete(0,END)
    price_input.insert(END,selected_item['values'][4])
    quantity_input.delete(0,END)
    quantity_input.insert(END,selected_item['values'][5])
    

#clear input
def clearinput():
    part_input.delete(0,END)
    customer_input.delete(0,END)
    retailer_input.delete(0,END)
    price_input.delete(0,END)
    quantity_input.delete(0,END)
   

#remove items from the table
def removeitem():
    index = selected_item['values'][0]
    db.remove(index)
    populate()

#used update a items in table
def updateitem():
    u_id = selected_item['values'][0]
    parts = part_input.get()
    customer = customer_input.get()
    retailer = retailer_input.get()
    price= price_input.get()
    quantity = quantity_input.get()
    db.update(u_id,parts,customer,retailer,price,quantity)
    populate()






#binding event to part_table
# Binding event to part_table
part_table.bind("<<TreeviewSelect>>", select_item)








# Function to apply a bold and attractive style to labels
def apply_style(label, fg_color):
    label.config(font=('bold', 14), pady=8, fg=fg_color)

# Part
part_text = StringVar()
part_label = Label(app, text="Parts name")
apply_style(part_label, 'blue')  # Blue text color
part_label.grid(row=0, column=0)
part_input = Entry(app, width=30, textvariable=part_text, font=('bold', 12))
part_input.grid(row=0, column=1, pady=8)

# Customer
customer_text = StringVar()
customer_label = Label(app, text="Customer name")
apply_style(customer_label, 'green')  # Green text color
customer_label.grid(row=0, column=2)
customer_input = Entry(app, width=30, textvariable=customer_text, font=('bold', 12))
customer_input.grid(row=0, column=3, pady=8)

# Retailer
retailer_text = StringVar()
retailer_label = Label(app, text="Name of Retailer")
apply_style(retailer_label, 'red')  # Red text color
retailer_label.grid(row=1, column=0)
retailer_input = Entry(app, width=30, textvariable=retailer_text, font=('bold', 12))
retailer_input.grid(row=1, column=1, pady=8)

# Price
price_text = IntVar()
price_label = Label(app, text="Price of the part")
apply_style(price_label, 'purple')  # Purple text color
price_label.grid(row=1, column=2)
price_input = Entry(app, width=15, textvariable=price_text, font=('bold', 12))
price_input.grid(row=1, column=3, pady=8)

# Quantity
quantity_text = IntVar()
quantity_label = Label(app, text="Number of parts")
apply_style(quantity_label, 'red')  # Purple text color
quantity_label.grid(row=1, column=4)
quantity_input = Entry(app, width=15, textvariable=quantity_text, font=('bold', 12))
quantity_input.grid(row=1, column=5, pady=8)


# Create scrollbar
scrollbar = Scrollbar(app)
scrollbar.grid(row=3, column=4, rowspan=6, sticky="NS")

# Set scrollbar to part_table
part_table.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=part_table.yview)

# Adding button
add_btn = Button(app, text='Add Item', width=20, command=additem)
add_btn.grid(row=2, column=0, pady=20)

remove_btn = Button(app, text='Remove Item', width=20, command=removeitem)
remove_btn.grid(row=2, column=1, pady=20)

update_btn = Button(app, text='Update Item', width=20, command=updateitem)
update_btn.grid(row=2, column=2, pady=20)

clearinput_btn = Button(app, text='Clear Input', width=20, command=clearinput)
clearinput_btn.grid(row=2, column=3, pady=20)

app.title("Part Manager")
app.geometry('1300x600')

# Populate the part_table with data
populate()

app.mainloop()



