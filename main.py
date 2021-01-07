from tkinter import  * #tkinter module for GUI
from tkinter import messagebox, Menu #for popup notification messgaebox
import requests # To send HTTP request and fetch the data using api link
import json #to parse over the fetched data
import sqlite3

pycrypto = Tk() # creating and instance TK
pycrypto.title("Pycrypto Portfolio")
pycrypto.iconbitmap('favicon.ico')

# DATABASE CODE ----------------------------------------------------------------------------------------------------

'''connecting DATABASE'''
con = sqlite3.connect('mycoin.db')
cursorObj = con.cursor() #creating cursor for parsing through db


'''CREATING TABLE '''
cursorObj.execute("CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY, symbol TEXT, amount INTEGER, price REAL)")
con.commit()


'''for taking our coins and data. executed once'''
# cursorObj.execute("INSERT INTO coin VALUES(1, 'BTC',2, 3000),(2,'ETH',10,2.05),(3,'LTC',75, 200),(4,'XMR',10,150)")

# con.commit()



# --------------------------------------------------------------------------------------------------

def reset():
    for cell in pycrypto.winfo_children():
        cell.destroy()

    app_nav()
    app_header()
    my_portfolio()



def app_nav():
    def clear_all():
        cursorObj.execute("DELETE FROM coin")
        con.commit()

        messagebox.showinfo("Portfolio Notification", "Portfolio Cleared - Add New Coins")
        reset()

    def close_app():
        pycrypto.destroy()

    menu = Menu(pycrypto)
    file_item = Menu(menu)
    file_item.add_command(label='Clear Portfolio', command=clear_all)
    file_item.add_command(label='Close App', command=close_app)
    menu.add_cascade(label="File", menu=file_item)
    pycrypto.config(menu=menu)

def my_portfolio():
    api_request = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=b9d1851a-1f1a-4781-8020-0fc880127dd6") #fetching the data using rquests module and storing the data in variable

    api = json.loads(api_request.content) #using json module to get parsable data using loads function and .content which help to deliver content of this api


    def font_color(Amount):
        if Amount>=0:
            return "green"
        else:
            return "red"

    def insert_coin():
        cursorObj.execute("INSERT INTO coin(symbol,price,amount) VALUES(?,?,?)", (symbol_txt.get(),price_txt.get(), amount_txt.get()))
        con.commit()
        messagebox.showinfo("Portfolio Notification", "Coin Added To Portfolio Successfully!")
        reset() 

    def update_coin():
        cursorObj.execute("UPDATE coin SET symbol=?, price=?, amount=? WHERE id=?", (symbol_update.get(), price_update.get(), amount_update.get(), portid_update.get()))
        con.commit()
        messagebox.showinfo("Portfolio Notification", "Coin Updated Successfully!")
        reset()

    def delete_coin():
        cursorObj.execute("DELETE FROM coin WHERE id=?", (portid_delete.get(),))
        messagebox.showinfo("Portfolio Notification", "Coin Deleted From Portfolio")
        con.commit()
        reset()


    cursorObj.execute("SELECT  *FROM coin") #fetching coin data from db
    coins = cursorObj.fetchall()


    
    total_pl = 0
    coin_row =1 #coin_row starting from 1 as 0 th row is for heading
    total_current_value = 0
    total_amount_paid = 0
    
    for i in range(0,300):   #to iterate over all the currency symbols and their price in our data
        for coin in coins: #to iterate over only those currency symbols and their price which I have invested.
            if api["data"][i]["symbol"]==coin[1]:
                total_paid = coin[2] * coin[3]
                current_value = coin[2] * api["data"][i]["quote"]["USD"]["price"]
                pl_percoin = api["data"][i]["quote"]["USD"]["price"] - coin[3]
                total_pl_coin = pl_percoin * coin[2]
                total_pl = total_pl + total_pl_coin
                total_current_value += current_value
                total_amount_paid +=  total_paid 
                

                portfolio_id = Label(pycrypto, text=coin[0], bg="#F3F4F6", fg="black", padx="2",pady="2",borderwidth="2", relief="groove") #label name with background and font color
                portfolio_id.grid(row=coin_row, column=0, sticky=N+S+W+E) #position in the grid in gui i.e. is top left and its type is sticky in North West South East

                name = Label(pycrypto, text=api["data"][i]["symbol"], bg="#F3F4F6", fg="black", padx="2",pady="2",borderwidth="2", relief="groove") #label name with background and font color
                name.grid(row=coin_row, column=1, sticky=N+S+W+E) #position in the grid in gui i.e. is top left and its type is sticky in North West South East

                price = Label(pycrypto, text="${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]), bg="#F3F4F6", fg="black", padx="2",pady="2",borderwidth="2", relief="groove") #label name with background and font color
                price.grid(row=coin_row, column=2, sticky=N+S+W+E) #position in the grid in gui i.e. is top left and its type is sticky in North West South East

                no_coins = Label(pycrypto, text=coin[2], bg="#F3F4F6", fg="black", padx="2",pady="2",borderwidth="2", relief="groove") #label name with background and font color
                no_coins.grid(row=coin_row, column=3, sticky=N+S+W+E) #position in the grid in gui i.e. is top left and its type is sticky in North West South East

                total_paid = Label(pycrypto, text="${0:.2f}".format(total_paid), bg="#F3F4F6", fg="black", padx="2",pady="2",borderwidth="2", relief="groove") #label name with background and font color
                total_paid.grid(row=coin_row, column=4, sticky=N+S+W+E) #position in the grid in gui i.e. is top left and its type is sticky in North West South East

                current_val = Label(pycrypto, text="${0:.2f}".format(current_value), bg="#F3F4F6", fg="black", padx="2",pady="2",borderwidth="2", relief="groove") #label name with background and font color
                current_val.grid(row=coin_row, column=5, sticky=N+S+W+E) #position in the grid in gui i.e. is top left and its type is sticky in North West South East

                pl_coin = Label(pycrypto, text="${0:.2f}".format(pl_percoin), bg="#F3F4F6", fg=font_color(float("{0:.2f}".format(pl_percoin))), padx="2",pady="2",borderwidth="2", relief="groove") #label name with background and font color
                pl_coin.grid(row=coin_row, column=6, sticky=N+S+W+E) #position in the grid in gui i.e. is top left and its type is sticky in North West South East

                totalpl= Label(pycrypto, text="${0:.2f}".format(total_pl_coin), bg="#F3F4F6", fg=font_color(float("{0:.2f}".format(total_pl_coin))), padx="2",pady="2",borderwidth="2", relief="groove") #label name with background and font color
                totalpl.grid(row=coin_row, column=7, sticky=N+S+W+E) #position in the grid in gui i.e. is top left and its type is sticky in North West South East
                

               
                coin_row +=1 #to change row for next iterration

    #insert data
    symbol_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    symbol_txt.grid(row=coin_row+1, column=1)

    price_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    price_txt.grid(row=coin_row+1, column=2)

    amount_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    amount_txt.grid(row=coin_row+1, column=3)

    #Add Coins button 
    Add_coin= Button(pycrypto, text="Add Coin", bg="#142E54", fg="white", command= insert_coin , font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2") #button name with background and font color
    Add_coin.grid(row=coin_row+1, column=4, sticky=N+S+W+E) #position in the grid in gui i.e. is top left and its type is sticky in North West South East   
   

    #update coin
    portid_update = Entry(pycrypto, borderwidth=2, relief="groove")
    portid_update.grid(row=coin_row+2, column=0)
    
    symbol_update = Entry(pycrypto, borderwidth=2, relief="groove")
    symbol_update.grid(row=coin_row+2, column=1)

    price_update = Entry(pycrypto, borderwidth=2, relief="groove")
    price_update.grid(row=coin_row+2, column=2)

    amount_update = Entry(pycrypto, borderwidth=2, relief="groove")
    amount_update.grid(row=coin_row+2, column=3)

    update_coin_txt = Button(pycrypto, text="Update Coin", bg="#142E54", fg="white", command=update_coin ,font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2")
    update_coin_txt.grid(row=coin_row + 2, column=4, sticky=N+S+E+W)

    #delete coin
    portid_delete = Entry(pycrypto, borderwidth=2, relief="groove")
    portid_delete.grid(row=coin_row+3, column=0)

    delete_coin_txt = Button(pycrypto, text="Delete Coin", bg="#142E54", fg="white", command=delete_coin ,font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2")
    delete_coin_txt.grid(row=coin_row+3, column=4, sticky=N+S+E+W)


    #Total for each column
    total_ap= Label(pycrypto, text="${0:.2f}".format(total_amount_paid), bg="#F3F4F6", fg="black", padx="2",pady="2",borderwidth="2", relief="groove") #label name with background and font color
    total_ap.grid(row=coin_row, column=4, sticky=N+S+W+E) #position in the grid in gui i.e. is top left and its type is sticky in North West South East   
    
    
    total_cv= Label(pycrypto, text="${0:.2f}".format(total_current_value), bg="#F3F4F6", fg="black", padx="2",pady="2",borderwidth="2", relief="groove") #label name with background and font color
    total_cv.grid(row=coin_row, column=5, sticky=N+S+W+E) #position in the grid in gui i.e. is top left and its type is sticky in North West South East   
    
    total_pl= Label(pycrypto, text="${0:.2f}".format(total_pl), bg="#F3F4F6", fg=font_color(float("{0:.2f}".format(total_pl))), padx="2",pady="2",borderwidth="2", relief="groove") #label name with background and font color
    total_pl.grid(row=coin_row, column=7, sticky=N+S+W+E) #position in the grid in gui i.e. is top left and its type is sticky in North West South East   
    
    api =""  #for emtying the data from api 

    #Buttons
   
    #Refresh button
    refresh= Button(pycrypto, text="Refresh", bg="#142E54", fg="white", command=reset, font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2") #button name with background and font color
    refresh.grid(row=coin_row+1, column=7, sticky=N+S+W+E) #position in the grid in gui i.e. is top left and its type is sticky in North West South East   
 
#First Row Heading Labeles : 
def app_header():
       
    portfolio_id= Label(pycrypto, text="Portfolio ID", bg="#142E54", fg="white", font="lato 12 bold", padx="5",pady="5", borderwidth="2", relief="groove") #label name with background and font color
    portfolio_id.grid(row=0, column=0, sticky=N+S+W+E) #position in the grid in gui i.e. is top left and its type is sticky in North West South East


    name = Label(pycrypto, text="Coin Name", bg="#142E54", fg="white", font="lato 12 bold", padx="5",pady="5", borderwidth="2", relief="groove") #label name with background and font color
    name.grid(row=0, column=1, sticky=N+S+W+E) #position in the grid in gui i.e. is top left and its type is sticky in North West South East

    price = Label(pycrypto, text="Price", bg="#142E54", fg="white", font="lato 12 bold", padx="5",pady="5", borderwidth="2", relief="groove") #label name with background and font color
    price.grid(row=0, column=2, sticky=N+S+W+E) #position in the grid in gui i.e. is top left and its type is sticky in North West South East

    no_coins = Label(pycrypto, text="Coins Owned", bg="#142E54", fg="white", font="lato 12 bold", padx="5",pady="5", borderwidth="2", relief="groove") #label name with background and font color
    no_coins.grid(row=0, column=3, sticky=N+S+W+E) #position in the grid in gui i.e. is top left and its type is sticky in North West South East

    total_paid = Label(pycrypto, text="Total Amount Paid", bg="#142E54", fg="white", font="lato 12 bold", padx="5",pady="5", borderwidth="2", relief="groove") #label name with background and font color
    total_paid.grid(row=0, column=4, sticky=N+S+W+E) #position in the grid in gui i.e. is top left and its type is sticky in North West South East

    current_val = Label(pycrypto, text="Current Value", bg="#142E54", fg="white", font="lato 12 bold", padx="5",pady="5", borderwidth="2", relief="groove") #label name with background and font color
    current_val.grid(row=0, column=5, sticky=N+S+W+E) #position in the grid in gui i.e. is top left and its type is sticky in North West South East

    pl_coin = Label(pycrypto, text="P/L Per Coin", bg="#142E54", fg="white", font="lato 12 bold", padx="5",pady="5", borderwidth="2", relief="groove") #label name with background and font color
    pl_coin.grid(row=0, column=6, sticky=N+S+W+E) #position in the grid in gui i.e. is top left and its type is sticky in North West South East

    totalpl= Label(pycrypto, text="Total P/L With Coin", bg="#142E54", fg="white", font="lato 12 bold", padx="5",pady="5", borderwidth="2", relief="groove") #label name with background and font color
    totalpl.grid(row=0, column=7, sticky=N+S+W+E) #position in the grid in gui i.e. is top left and its type is sticky in North West South East


''' If you want to clear database manually'''
# cursorObj.execute("DELETE FROM coin")
# con.commit()

app_nav()
app_header()
my_portfolio()#calling the function

pycrypto.mainloop() #All the code in mainloop will execute until window is open

cursorObj.close()
con.close()