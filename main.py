from customtkinter import set_appearance_mode

from GUI.AppGUI import AppGUI

if __name__ == '__main__':
    app = AppGUI()

    app.title('Kryptologické Šifry')
    app.geometry('650x500')
    app.resizable(width=False, height=False)
    set_appearance_mode('Dark')

    app.mainloop()
