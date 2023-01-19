import math
import pandas as pd
import customtkinter as ct
import requests, time
from tkinter import *
import tkinter.messagebox
from datetime import datetime, timedelta

# Modes: "System" (standard), "Dark", "Light"
ct.set_appearance_mode("System")
# Themes: "blue" (standard), "green", "dark-blue"
ct.set_default_color_theme("blue")

def main():

    app = ct.CTk()
    app.title("PAYEND")
    app.iconbitmap('C:\\Users\\Raghav Desai\\Documents\\My Files\\Python\\Project_For_Fun\\PAYEND 4.7.2\\PAYEND_ico.ico')
    app.geometry(f"{785}x{480}")

    # initialize variables
    range = IntVar(app)
    range.set('365')
    my_dict = {"Nifty 50":9, "Nifty Bank":23,"Nifty IT":19,"Nifty PSU Bank":43,"Nifty Auto":52,"Nifty Metal":51,"Nifty Fin Service":47}
    range_for = {"Range For Today":"o", "Range For Tommorow":"c"}


    #============ Functions ============
    def dateToTimeStamp(date):
        time_tuple = date.timetuple()
        timestamp = round(time.mktime(time_tuple))
        return timestamp
    
    # Declaring start & end date
    start = dateToTimeStamp(datetime.today() - timedelta(days = 1))
    end = dateToTimeStamp(datetime.today())

    def Calculation():
        try:
            url_vix_price = "https://priceapi.moneycontrol.com/techCharts/history?symbol=" + str(36) + "&resolution=1D&from=" + str(start) + "&to=" + str(end)
            url_stock_price = "https://priceapi.moneycontrol.com/techCharts/history?symbol=" + str(my_dict[E1.get()]) + "&resolution=1D&from=" + str(start) + "&to=" + str(end)
            prtg = round(float(pd.DataFrame(requests.get(url_vix_price).json())[range_for[L2.get()]]) / round(math.sqrt(range.get()), 4), 2)
            cal = round((float(pd.DataFrame(requests.get(url_stock_price).json())[range_for[L2.get()]]) * prtg) * 0.01, 4)
            calculation_1 = str(round(float(pd.DataFrame(requests.get(url_stock_price).json())[range_for[L2.get()]]) + cal, 0))
            calculation_2 = str(round(float(pd.DataFrame(requests.get(url_stock_price).json())[range_for[L2.get()]]) - cal, 0))
            main.L4.configure(text='Upper Limit : ' + calculation_1)
            main.L5.configure(text='Lower Limit : ' + calculation_2)
            # Calling round Upper(UL) & Lower(LL) classes
            UL(math.floor(float(pd.DataFrame(requests.get(url_stock_price).json())[range_for[L2.get()]]) + cal))
            LL(math.floor(float(pd.DataFrame(requests.get(url_stock_price).json())[range_for[L2.get()]]) - cal))
        except KeyError:
            main.L4.configure(text="Can't fatch Data!")
            main.L5.configure(text="Pls select indices")
        except ValueError:
            if datetime.now().strftime("%A") == "Saturday" or "Sunday":
                main.L4.configure(text="🗓️" + datetime.now().strftime("%A"))
                main.L4a.configure(text="Today is Holiday")
                main.L5.configure(text="Have a nice weekend.")
            else:
                main.L4.configure(text="Can't fatch Data!")
                main.L5.configure(text="Range didn't shown at the movement")
                main.L4a.configure(text="Pls wait till 09:15 AM")

        except requests.exceptions.ConnectionError:
            main.L4.configure(text='Link Not Working! 🌐')
            main.L5.configure(text="Pls check internet connection...")

    def UL(n):
        U_digits = math.log10(n) + 1
        U_first = n // 1000
        U_middle = int((n // math.pow(10, U_digits // 2))) % 10
        if (U_middle == 9):
            U_first += 1
            final1 = str(U_first) + str('000')
            # Displaying data on window
            main.L4a.configure(text='≈ ' + final1)
        else:
            U_middle += 1
            final1 = str(U_first) + str(U_middle) + str('00')
            # Displaying data on window
            main.L4a.configure(text='≈ ' + final1)

    def LL(n):
        L_digits = math.log10(n) + 1
        L_first = n // 1000
        L_middle = int((n // math.pow(10, L_digits // 2))) % 10
        final2 = str(L_first)+str(L_middle) + str('00')
        # Displaying data on window
        main.L5a.configure(text='≈ ' + final2)

    def vix_indicator():
        try:
            url = "https://priceapi.moneycontrol.com/techCharts/history?symbol=36&resolution=1D&from="+str(start)+"&to="+str(end)
            vix = float(pd.DataFrame(requests.get(url).json())[range_for[L2.get()]])
            if 10 < vix <= 15:
                main.Btn.configure(text_color="#FFFF00", text=vix, hover="disabled")#yellow
            elif 15 < vix <= 22:
                main.Btn.configure(text_color="#00FF00", text=vix, hover="disabled")#green
            elif 23 < vix <= 25:
                main.Btn.configure(text_color="#FFA500", text=vix, hover="disabled")#orange
            elif 26 <= vix:
                main.Btn.configure(text_color="#FF0000", text=vix, hover="disabled")#red
        except ValueError:
            if datetime.now().strftime("%A") == "Saturday" or "Sunday":
                main.L4.configure(text="🗓️" + datetime.now().strftime("%A"))
                main.L4a.configure(text="Today is Holiday")
                main.L5.configure(text="Have a nice weekend.")
            else:
                main.L4.configure(text="Can't fatch Data!")
                main.L4a.configure(text="Range didn't shown at the movement")
                main.L5.configure(text="Pls wait till 09:15 AM")
        except requests.exceptions.ConnectionError:
            main.L4.configure(text='Link Not Working! 🌐')
            main.L5.configure(text="Pls check internet connection...")
        
    def change_appearance_mode(new_mode):
        ct.set_appearance_mode(new_mode)

    def Date():
        date = ct.CTkLabel(frame_left, text= datetime.now().date(), font=("Roboto Medium", -13))
        date.grid(row=2,  pady=20, sticky=S)

    def on_closing():
        app.destroy()

    # ============ create two frames ============
    # configure grid layout (2x1)
    app.grid_columnconfigure(1, weight=1)
    app.grid_rowconfigure(0, weight=1)

    frame_left = ct.CTkFrame(app, width=180, corner_radius=0)
    frame_left.grid(row=0, column=0, sticky="nswe")

    frame_right = ct.CTkFrame(app)
    frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)


    # ============ frame_left ============
    Main_label = ct.CTkLabel(frame_left,
                                    text="PAYEND 4.7.2",
                                    font=("Roboto Medium", -16))
    Main_label.grid(row=1, column=0, pady=17, padx=17)

    label_mode = ct.CTkLabel(frame_left, text="Appearance Mode:")
    label_mode.grid(row=3, column=0, pady=0, padx=20, sticky="w")

    appearance_mode = ct.CTkOptionMenu(frame_left,
                                            values=["System","Light", "Dark"],
                                            command=change_appearance_mode)
    appearance_mode.grid(row=4, column=0, pady=10, padx=20, sticky="w")
    
    # Vix indicator inputs
    main.Btn = ct.CTkButton(frame_left, text="Today's Vix", command=vix_indicator)
    main.Btn.grid(row=6, pady=20, padx=20, sticky="we")


    # ============ frame_right ============
    # configure grid layout (3x7)
    frame_right.rowconfigure((0, 1, 2, 3), weight=1)
    frame_right.rowconfigure(7, weight=10)
    frame_right.columnconfigure((0, 1), weight=1)
    frame_right.columnconfigure(2, weight=0)

    frame_info = ct.CTkFrame(frame_right)
    frame_info.grid(columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")

    # ============ frame_info ============
    # configure grid layout (1x1)
    frame_info.rowconfigure(0, weight=1)
    frame_info.columnconfigure(0, weight=1)

    label_info_1 = ct.CTkLabel(frame_info,
                                        text="This Market Range Specifier will show you the\n" +
                                        "market range upto which the market will move \n" +
                                        "today. You can also see Weekly & Monthly Range.",
                                        height=110, corner_radius=6, fg_color=("white", "gray38"),
                                        justify=tkinter.LEFT)
    label_info_1.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

    # ============ frame_right ============
    L1 = ct.CTkLabel(frame_right, text="Market Range For :")
    L1.grid(row=4, column=0, pady=10, padx=20, sticky="w")

    E1 = ct.CTkOptionMenu(frame_right,values=list(my_dict.keys()))
    E1.grid(row=4, column=1, pady=10, padx=20, sticky="w")

    L2 = ct.CTkSegmentedButton(frame_right, values=list(range_for.keys()))
    L2.grid(row=5, column=0, columnspan=2, pady=10, padx=10, sticky=N+S+E+W)
 
    L3 = ct.CTkLabel(frame_right,text="Range Limit -")
    L3.grid(row=0, column=2, columnspan=1, pady=15, padx=4, sticky="w")

    s = ct.CTkRadioButton(frame_right, text='Day',
                                    variable=range,
                                    value=365)
    s.grid(row=1, column=2, pady=6, padx=6, sticky="n")

    s = ct.CTkRadioButton(frame_right, text='Week',
                                    variable=range,
                                    value=52)
    s.grid(row=2, column=2, pady=6, padx=6, sticky="n")

    s = ct.CTkRadioButton(frame_right, text='Month',
                                    variable=range,
                                    value=12)
    s.grid(row=3, column=2, pady=6, padx=6, sticky="n")

    B = ct.CTkButton(frame_right, text="Show range", border_width=2,
        fg_color=None, command=Calculation)
    B.grid(row=5, column=2, columnspan=1, pady=20, padx=20, sticky="we")

    main.L4 = ct.CTkLabel(
        frame_right, text="Upper limit :")
    main.L4.grid(row=6, column=0, pady=1, padx=10, sticky="w")

    main.L4a = ct.CTkLabel(frame_right, text="")
    main.L4a.grid(row=6, column=1, pady=1, padx=10, sticky="w")

    main.L5 = ct.CTkLabel(frame_right, text="Lower limit :")
    main.L5.grid(row=7, column=0, pady=1, padx=10, sticky="w")

    main.L5a = ct.CTkLabel(frame_right, text="")
    main.L5a.grid(row=7, column=1, pady=1, padx=10, sticky="w")

    # set initial value
    appearance_mode.set("System")
    L2.set("Range For Today")
    E1.set('Select Indice')

    # call .on_closing() when app gets closed
    app.protocol("WM_DELETE_WINDOW",on_closing)
    app.after(50, Date)
    app.mainloop()
main()