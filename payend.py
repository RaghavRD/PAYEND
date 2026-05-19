import math
import requests
import yfinance as yf
from tkinter import *
import tkinter.messagebox
import customtkinter as ct
from datetime import datetime, timedelta

# Maps app label names → Yahoo Finance ticker symbols
_YF_SYMBOLS = {
    "INDIAVIX":          "^INDIAVIX",
    "Nifty 50":          "^NSEI",
    "Nifty Bank":        "^NSEBANK",
    "Nifty IT":          "^CNXIT",
    "Nifty PSU Bank":    "^CNXPSUBANK",
    "Nifty Auto":        "^CNXAUTO",
    "Nifty Metal":       "^CNXMETAL",
    "Nifty Fin Service": "^CNXFIN",
}

def get_history(symbol, start, end, **_):
    yf_symbol = _YF_SYMBOLS.get(symbol, symbol)
    ticker = yf.Ticker(yf_symbol)
    # Fetch 7 days back so weekends/holidays don't produce an empty DataFrame
    df = ticker.history(
        start=(start - timedelta(days=7)).strftime("%Y-%m-%d"),
        end=(end + timedelta(days=1)).strftime("%Y-%m-%d"),
    )
    return df

# Modes: "System" (standard), "Dark", "Light"
ct.set_appearance_mode("System")
# Themes: "blue" (standard), "green", "dark-blue"
ct.set_default_color_theme("blue")

def main():

    app = ct.CTk()
    app.title("PAYEND")
    try:
        _icon = PhotoImage(file='faviconn.png')
        app.iconphoto(True, _icon)
    except Exception:
        pass
    app.geometry(f"{785}x{480}")

    # initialize variables
    range = IntVar(app)
    range.set('365')
    index_list = ["Nifty 50","Nifty Bank","Nifty IT","Nifty PSU Bank","Nifty Auto","Nifty Metal","Nifty Fin Service"]
    range_for = {"Range For Today":"Open", "Range For Tommorow":"Close"}

    # Declaring start & end date
    start_d = datetime.today()
    end_d = datetime.today()

    # ============ Functions ============

    def Calculation():
        try:
            col = range_for[L2.get()]
            url_vix_price   = get_history(symbol="INDIAVIX", start=start_d, end=end_d)
            url_stock_price = get_history(symbol=E1.get(),   start=start_d, end=end_d)
            vix_val   = float(url_vix_price[col].iloc[-1])
            stock_val = float(url_stock_price[col].iloc[-1])
            prtg = round(vix_val / round(math.sqrt(range.get()), 4), 2)
            cal  = round((stock_val * prtg) * 0.01, 4)
            stock_upper_level = round(stock_val + cal, 2)
            stock_lower_level = round(stock_val - cal, 2)
            main.L4.configure(text='Upper Limit : ' + str(stock_upper_level))
            main.L5.configure(text='Lower Limit : ' + str(stock_lower_level))
            UL(math.floor(stock_val + cal))
            LL(math.floor(stock_val - cal))
        except KeyError:
            main.L4.configure(text="Can't fatch Data!")
            main.L5.configure(text="Pls select indices")
            main.L4a.configure(text="")
            main.L5a.configure(text="")
        except (TypeError, ValueError, IndexError):
            if start_d.strftime("%A") == "Saturday" or datetime.now().strftime("%A") == "Sunday":
                main.L4.configure(text="🗓️" + datetime.now().strftime("%A"))
                main.L4a.configure(text="Today is Holiday")
                main.L5.configure(text="Have a nice weekend.")
                main.L5a.configure(text="")
            elif start_d.time() > datetime.strptime("09:15:00", "%H:%M:%S").time():
                main.L4.configure(text="🗓️" + start_d.strftime("%A") +', '+ str(start_d.strftime("%d %b")))
                main.L4a.configure(text="Today is Holiday")
                main.L5.configure(text="")
                main.L5a.configure(text="")
            else:
                main.L4.configure(text="Can't fatch Data!")
                main.L5.configure(text="Pls wait till 09:15 AM")
                main.L4a.configure(text="🔗🔗🔗 🔗🔗🔗")
                main.L5a.configure(text="")
        except requests.exceptions.ConnectionError:
            main.L4.configure(text='Link Not Working! 🌐')
            main.L5.configure(text="Pls check internet connection...")
            main.L4a.configure(text="")
            main.L5a.configure(text="")

    def UL(n):
        U_digits = math.log10(n) + 1
        U_first = n // 1000
        U_middle = int((n // math.pow(10, U_digits // 2))) % 10
        if (U_middle == 9):
            U_first += 1
            final1 = str(U_first) + str('000')
            main.L4a.configure(text='≈ ' + final1)
        else:
            U_middle += 1
            final1 = str(U_first) + str(U_middle) + str('00')
            main.L4a.configure(text='≈ ' + final1)

    def LL(n):
        L_digits = math.log10(n) + 1
        L_first = n // 1000
        L_middle = int((n // math.pow(10, L_digits // 2))) % 10
        final2 = str(L_first)+str(L_middle) + str('00')
        main.L5a.configure(text='≈ ' + final2)

    def vix_indicator():
        try:
            col = range_for[L2.get()]
            url = get_history(symbol="INDIAVIX", start=start_d, end=end_d)
            vix = round(float(url[col].iloc[-1]), 2)
            if vix <= 10:
                main.Btn.configure(text_color="#FF4040", text=vix, hover="disabled")#red
            elif 10 < vix <= 15:
                main.Btn.configure(text_color="#F5B041", text=vix, hover="disabled")#light green
            elif 15 < vix <= 22:
                main.Btn.configure(text_color="#00FF00", text=vix, hover="disabled")#green
            elif 22 < vix <= 25:
                main.Btn.configure(text_color="#FFA500", text=vix, hover="disabled")#orange
            elif vix >= 26:
                main.Btn.configure(text_color="#FF0000", text=vix, hover="disabled")#red
        except (TypeError, ValueError, IndexError):
            if datetime.now().strftime("%A") == "Saturday" or datetime.now().strftime("%A") == "Sunday":
                main.L4.configure(text="🗓️" + datetime.today().strftime("%A"))
                main.L4a.configure(text="Today is Holiday")
                main.L5.configure(text="Have a nice weekend.")
                main.L5a.configure(text="")
            elif datetime.now().time() > datetime.strptime("09:15:00", "%H:%M:%S").time():
                main.L4.configure(text="🗓️" + datetime.now().strftime("%A") +', '+ str(datetime.now().strftime("%d %b")))
                main.L4a.configure(text="Today is Holiday")
                main.L5.configure(text="")
                main.L5a.configure(text="")
            else:
                main.L4.configure(text="Can't fatch Data!")
                main.L5.configure(text="Pls wait till 09:15 AM")
                main.L4a.configure(text="🔗🔗🔗 🔗🔗🔗")
                main.L5a.configure(text="")
        except requests.exceptions.ConnectionError:
            main.L4.configure(text='Link Not Working! 🌐')
            main.L5.configure(text="Pls check internet connection...")
            main.L4a.configure(text="")
            main.L5a.configure(text="")

    def change_appearance_mode(new_mode):
        ct.set_appearance_mode(new_mode)

    def Date():
        date = ct.CTkLabel(frame_left, text= start_d.date(), font=("Roboto Medium", -13))
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
                                    text="RAVIO 4.7.6",
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

    E1 = ct.CTkOptionMenu(frame_right,values= index_list)
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

    main.L4 = ct.CTkLabel(frame_right, text="Upper limit :")
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
    E1.set("Select Indice")

    # call .on_closing() when app gets closed
    app.protocol("WM_DELETE_WINDOW",on_closing)
    app.after(50, Date)
    app.mainloop()
main()
