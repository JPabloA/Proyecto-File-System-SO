from tkinter import Tk, Canvas, Entry, Text, Button

class FileSystem_GUI(Tk):
    def __init__(self):
        super().__init__()

        self.geometry("750x550")
        self.configure(bg = "#FFFFFF")

        canvas = Canvas(
            self,
            bg = "#FFFFFF",
            height = 550,
            width = 750,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        # Label "Buscador"
        canvas.place(x = 0, y = 0)
        canvas.create_text( 9, 445.0, anchor="nw", text="Buscador", fill="#000000", font=("Inter", 13 * -1) )

        # Text input: Directory path
        textInput_DirectoryPath = Entry( bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0 )
        textInput_DirectoryPath.place( x=9.0, y=11.0, width=722.0, height=37.0 )

        # Text input: Search bar
        textInput_SearchBar = Entry( bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0 )
        textInput_SearchBar.place( x=9.0, y=465.0, width=150.0, height=30.0 )

        # Text area: Display
        textArea_Display = Text( bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0 )
        textArea_Display.place( x=173.0, y=72.0, width=558.0, height=459.0 )


        button_1 = Button( text="Crear Disco", command=lambda: print("button_1 clicked"), relief="flat" )
        button_1.place( x=9.0, y=72.0, width=150.0, height=35.0 )

        button_2 = Button( text="Crear Directorio", borderwidth=0, command=lambda: print("button_2 clicked"), relief="flat" )
        button_2.place( x=9.0, y=119.0, width=150.0, height=35.0 )

        button_3 = Button( text="Crear Archivo", borderwidth=0, command=lambda: print("button_3 clicked"), relief="flat" )
        button_3.place( x=9.0, y=166.0, width=150.0, height=35.0 )

        button_4 = Button( text="Desp. Árbol", borderwidth=0, command=lambda: print("button_4 clicked"), relief="flat" )
        button_4.place( x=9.0, y=213.0, width=150.0, height=35.0 )

        button_5 = Button( text="Buscar", borderwidth=0, command=lambda: print("button_5 clicked"), relief="flat" )
        button_5.place( x=9.0, y=503.0, width=150.0, height=30.0 )

if __name__ == "__main__":
    app = FileSystem_GUI()

    app.resizable(False, False)
    app.mainloop()

