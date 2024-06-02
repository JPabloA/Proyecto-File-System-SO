from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel
class CopyFiles(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Copy Files")
        self.geometry("750x593")
        self.configure(bg="#FFFFFF")
        self.resizable(False, False)

        canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=593,
            width=750,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)

        # Text input: Directory path (Origin)
        self.entry_1 = Entry(
            self,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_1.insert("1.0", "ORIGEN")
        self.entry_1.place(x=14.0, y=45.0, width=722.0, height=33.0)

        # Text input: Directory path (Destiny)
        self.entry_2 = Entry(
            self,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_2.insert("1.0", "DESTINO")
        self.entry_2.place(x=14.0, y=146.0, width=722.0, height=33.0)

        # Button: First method to copy
        self.button_1 = Button(
            self,
            text = "Ruta real a ruta virtual",
            borderwidth=0,
            highlightthickness=0,
            command=self.button_1_clicked,
            relief="flat"
        )
        self.button_1.place(x=14.0, y=219.0, width=310.0, height=49.0)

        # Button: Second method to copy
        self.button_2 = Button(
            self,
            text = "Ruta virtual a ruta real",
            borderwidth=0,
            highlightthickness=0,
            command=self.button_2_clicked,
            relief="flat"
        )
        self.button_2.place(x=14.0, y=277.0, width=310.0, height=49.0)

        # Button: Third method to copy
        self.button_3 = Button(
            self,
            text = "Ruta virtual a ruta virtual",
            borderwidth=0,
            highlightthickness=0,
            command=self.button_3_clicked,
            relief="flat"
        )
        self.button_3.place(x=14.0, y=335.0, width=310.0, height=49.0)

        canvas.create_text(
            14.0,
            19.0,
            anchor="nw",
            text="Copiar desde:",
            fill="#000000",
            font=("Inter", 16 * -1)
        )

        canvas.create_text(
            14.0,
            118.0,
            anchor="nw",
            text="Hasta:",
            fill="#000000",
            font=("Inter", 16 * -1)
        )

    def button_1_clicked(self):
        print("button_1 clicked")

    def button_2_clicked(self):
        print("button_2 clicked")

    def button_3_clicked(self):
        print("button_3 clicked")
