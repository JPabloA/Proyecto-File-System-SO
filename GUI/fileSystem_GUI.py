import window_ShowTree, move_GUI
from tkinter import SINGLE, Tk, Canvas, Entry, Button, Listbox

class FileSystem_GUI(Tk):
    def __init__(self):
        super().__init__()

        self.title("File system custom - OS")
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
        textArea_Display = Listbox( bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0, selectmode=SINGLE, font="Arial 14" )
        textArea_Display.place( x=173.0, y=72.0, width=558.0, height=459.0 )
        textArea_Display.bind("<Button-3>", self.__contentDisplayRightClick)

        self.__loadContentInFSDisplay(textArea_Display)

        button_1 = Button( text="Crear Disco", command=lambda: print("button_1 clicked"), relief="flat" )
        button_1.place( x=9.0, y=72.0, width=150.0, height=35.0 )

        button_2 = Button( text="Crear Directorio", borderwidth=0, command=self.display_Move_GUI, relief="flat" )
        button_2.place( x=9.0, y=119.0, width=150.0, height=35.0 )

        button_3 = Button( text="Crear Archivo", borderwidth=0, command=lambda: print("button_3 clicked"), relief="flat" )
        button_3.place( x=9.0, y=166.0, width=150.0, height=35.0 )

        button_4 = Button( text="Desp. Árbol", borderwidth=0, command=self.display_WindowShowTree, relief="flat" )
        button_4.place( x=9.0, y=213.0, width=150.0, height=35.0 )

        button_5 = Button( text="Buscar", borderwidth=0, command=lambda: print("button_5 clicked"), relief="flat" )
        button_5.place( x=9.0, y=503.0, width=150.0, height=30.0 )

    def __contentDisplayRightClick(self, event):
        print(event)

    def __loadContentInFSDisplay(self, display: Listbox):
        # TODO: Gather files and folders
        content = ["Carpeta1", "Carpeta2", "Carpeta3", "File1", "File2"]

        for i in range(0, len(content)):
            display.insert(i, content[i])

    def display_Move_GUI(self):
        window = move_GUI.Move_GUI(self)
        window.grab_set()

    def display_WindowShowTree(self):
        window = window_ShowTree.Window_ShowTree(self)
        window.grab_set()

if __name__ == "__main__":
    app = FileSystem_GUI()

    app.resizable(False, False)
    app.mainloop()

