from tkinter import Tk, Canvas, Entry, Text, Button

class Move_GUI(Tk):
    def __init__(self):
        super().__init__()

        self.geometry("750x593")
        self.configure(bg = "#FFFFFF")

        canvas = Canvas(
            self,
            bg = "#FFFFFF",
            height = 593,
            width = 750,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        canvas.place(x = 0, y = 0)
        
        # Labels
        canvas.create_text( 9.0, 14.0, anchor="nw", text="Mover archivo/directorio:", fill="#000000", font=("Inter", 16 * -1) )
        canvas.create_text( 9.0, 98.0, anchor="nw", text="Hasta:", fill="#000000", font=("Inter", 16 * -1) )

        # Text input: Directory path
        textInput_SearchBar = Entry( bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0 )
        textInput_SearchBar.place( x=9.0, y=40.0, width=722.0, height=33.0 )

        # Text input: Directory path 2
        textInput_SearchBar2 = Entry( bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0 )
        textInput_SearchBar2.place( x=9.0, y=126.0, width=722.0, height=33.0 )

        # Buttons
        button_1 = Button( text="Mover", borderwidth=0, highlightthickness=0, command=lambda: print("button_1 clicked"), relief="flat" )
        button_1.place( x=9.0, y=196.0, width=203.0, height=49.0 )

        button_2 = Button( text="Cancelar", borderwidth=0, highlightthickness=0, command=lambda: print("button_2 clicked"), relief="flat" )
        button_2.place( x=9.0, y=270.0, width=203.0, height=49.0 )

if __name__ == "__main__":
    app = Move_GUI()

    app.resizable(False, False)
    app.mainloop()

