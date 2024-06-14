from tkinter import Canvas, Entry, Button, Toplevel, messagebox
from src.file import File
from src.directory import Directory
import os

class CopyFiles(Toplevel):
    def __init__(self, parent, selected_obj: File | Directory = None, selected_path: str = ""):
        super().__init__(parent)

        self.parent = parent
        self.selected_obj = selected_obj
        self.isFile = True

        path_origin: str = ""
        if selected_obj is not None:
            if isinstance(selected_obj, File):
                path_origin = (selected_path if selected_path else f"{self.parent.fileSystem.getCurrentWorkingDirectory()}/") + f"{selected_obj.name}.{selected_obj.extension}"
                self.isFile = True
            elif isinstance(selected_obj, Directory):
                path_origin = (selected_path if selected_path else f"{self.parent.fileSystem.getCurrentWorkingDirectory()}/") + f"{selected_obj.name}"
                self.isFile = False
            else:
                print("Object could not be recognized")
                return

        self.title("Copy Files")
        self.geometry("750x405")
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
        self.entry_Origin = Entry( self, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0 )
        self.entry_Origin.insert(0, path_origin)
        self.entry_Origin.place(x=14.0, y=45.0, width=722.0, height=33.0)

        # Text input: Directory path (Destiny)
        self.entry_Destiny = Entry( self, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0 )
        self.entry_Destiny.insert(0, "/root/")
        self.entry_Destiny.place(x=14.0, y=146.0, width=722.0, height=33.0)

        # Button: First method to copy
        self.button_1 = Button( self, text = "Ruta real a ruta virtual", borderwidth=0, highlightthickness=0, command=self.__copy_RealToVirtual, relief="flat" )
        self.button_1.place(x=14.0, y=219.0, width=310.0, height=49.0)

        # Button: Second method to copy
        self.button_2 = Button( self, text = "Ruta virtual a ruta real", borderwidth=0, highlightthickness=0, command=self.__copy_VirtualToReal, relief="flat" )
        self.button_2.place(x=14.0, y=277.0, width=310.0, height=49.0)

        # Button: Third method to copy
        self.button_3 = Button( self, text = "Ruta virtual a ruta virtual", borderwidth=0, highlightthickness=0, command=self.__copy_VirtualToVirtual, relief="flat" )
        self.button_3.place(x=14.0, y=335.0, width=310.0, height=49.0)

        canvas.create_text( 14.0, 19.0, anchor="nw", text="Copiar desde:", fill="#000000", font=("Inter", 16 * -1) )
        canvas.create_text( 14.0, 118.0, anchor="nw", text="Hasta:", fill="#000000", font=("Inter", 16 * -1) )

        if self.parent.fileSystem.disk is None:
            messagebox.showwarning("No se encontro ningún disco", "Asegúrese de crear un disco antes de copiar un archivo al file system")
            self.entry_Origin.config( state="disabled" )
            self.entry_Destiny.config( state="disabled" )
            self.button_1.config( state="disabled" )
            self.button_2.config( state="disabled" )
            self.button_3.config( state="disabled" )

    def __getInputPaths(self):
        path_origin: str  = self.entry_Origin.get()
        path_destiny: str = self.entry_Destiny.get()

        # Make sure the path_destiny finishes with "/"
        path_destiny += "/" if path_destiny[-1] != "/" else ""

        return path_origin, path_destiny

    def __copy_DirectoryContentRecursively(self, directory_origin: Directory, directory_destiny: Directory):
        # Copy its files in the directory_destiny
        for file in directory_origin.files.values():
            file_name = file.name
            file_extension = file.extension
            file_content = file.content

            self.parent.fileSystem.createFile( file_name, file_extension, file_content, directory_destiny )

        # Copy its directories in the directory_destiny
        for subdirectory in directory_origin.directories.values():
            dir_name = subdirectory.name
            self.parent.fileSystem.createDirectory( dir_name, directory_destiny )

        for sub_origin, sub_destiny in zip(directory_origin.directories.values(), directory_destiny.directories.values()):
            self.__copy_DirectoryContentRecursively( sub_origin, sub_destiny )

    def __copy_RealToVirtual(self):
        path_origin, path_destiny = self.__getInputPaths()
        directory_destiny = self.parent.fileSystem.navigateToDirectory(path_destiny)

        if directory_destiny is None:
            messagebox.showerror("Directorio destino no existe", "El directorio de destino no pudo ser encontrado, por favor ingrese una ruta válida")
            return

        def copy_file(src, dest_dir, direct_copy: bool = True):
            file_name = os.path.basename(src)
            name, extension = os.path.splitext(file_name)
            extension = extension.lstrip('.')

            with open(src, 'r') as archivo:
                file_content = archivo.read().strip()

            if not self.parent.isUniqueInDestinyDir(f"{name}.{extension}", "File", path_destiny) and direct_copy:
                answer = messagebox.askyesno("Archivo existe en el destino", "Existe un archivo con el mismo nombre en el destino. ¿Desea sobreescribir su contenido?")
                if answer:
                    selected_file: File = self.parent.getFileObj( f"{name}.{extension}", path_destiny )

                    oldSectorsList = self.parent.fileSystem.fat.getFileSectors( selected_file.fat_index )
                    newSectorsList = self.parent.fileSystem.disk.writeToDisk( file_content, oldSectorsList )
                    if (newSectorsList == []):
                        return
                    self.parent.fileSystem.fat.freeFATEntries( selected_file.fat_index )
                    newStartingIndex = self.parent.fileSystem.fat.assingSectorList(newSectorsList)

                    selected_file.modifyContent( name, extension, file_content )
                    selected_file.assignSectors( newStartingIndex )
                    return True
            else:
                try:
                    self.parent.fileSystem.createFile(name, extension, file_content, dest_dir)
                    return True
                except ValueError as e:
                    messagebox.showerror("Error al copiar archivo", str(e))
                    return False
            return False

        def copy_directory(src, dest_dir):
            dir_name = os.path.basename(os.path.normpath(src))

            if not self.parent.isUniqueInDestinyDir(dir_name, "Directory", path_destiny):
                answer = messagebox.askyesno("Directorio existe en el destino", "Existe un directorio con el mismo nombre en el destino. ¿Desea sobreescribir su contenido?")
                if answer:
                    selected_dir: Directory = self.parent.getDirObj( dir_name, path_destiny )
                    self.parent.fileSystem.clearDirectory (selected_dir)

                    directory_destiny.directories.pop( dir_name )
                else:
                    return False

            new_directory = self.parent.fileSystem.createDirectory(dir_name, dest_dir)

            for item in os.listdir(src):
                item_path = os.path.join(src, item)
                if os.path.isfile(item_path):
                    copy_file(item_path, new_directory, False)
                elif os.path.isdir(item_path):
                    copy_directory(item_path, new_directory)
            return True

        obj_type: str = ""
        result = False
        if os.path.isfile(path_origin):
            result = copy_file(path_origin, directory_destiny)
            obj_type = "Archivo"
        elif os.path.isdir(path_origin):
            result = copy_directory(path_origin, directory_destiny)
            obj_type = "Directorio"
        else:
            messagebox.showwarning("Copy", "Tipo de archivo no compatible")

        if result:
            messagebox.showinfo(f"Acción completada", f"El {obj_type} fue copiado con éxito")
            self.destroy()

        self.parent.updateDiskState()
        self.parent.reloadFileSystem()

    def __copy_VirtualToReal(self):
        if self.selected_obj is None:
            messagebox.showerror("No existe ningún objeto seleccionado", "La ruta ingresada no corresponde a ningún objeto dentro del file system")
            return

        path_origin, path_destiny = self.__getInputPaths()

        def copy_file_virtual_to_real(file, dest):
            file_name = f"{file.name}.{file.extension}"
            file_path = os.path.join(dest, file_name)

            if os.path.isfile(file_path):
                overwrite = messagebox.askyesno("Archivo existe en el destino", f"Existe un archivo con el nombre {file_name} en el destino. ¿Desea sobrescribirlo?")
                if not overwrite:
                    return False

            with open(file_path, 'w') as archivo:
                archivo.write(file.content)
            return True

        def copy_directory_virtual_to_real(directory, dest):
            dir_path = os.path.join(dest, directory.name)

            if os.path.isdir(dir_path):
                overwrite = messagebox.askyesno("Directorio existe en el destino", f"Existe un directorio con el nombre {directory.name} en el destino. ¿Desea sobrescribirlo?")
                if not overwrite:
                    return False
                else:
                    # Remove the existing directory if the user chose to overwrite it
                    import shutil
                    shutil.rmtree(dir_path)

            os.makedirs(dir_path, exist_ok=True)

            for file in directory.getFiles().values():
                copy_file_virtual_to_real(file, dir_path)
            for subdirectory in directory.getDirectories().values():
                copy_directory_virtual_to_real(subdirectory, dir_path)

            return True
        obj_type: str = ""
        result = False
        if self.isFile:
            obj_type = "Archivo"
            result = copy_file_virtual_to_real(self.selected_obj, path_destiny)
        else:
            obj_type = "Directorio"
            result = copy_directory_virtual_to_real(self.selected_obj, path_destiny)

        if result:
            messagebox.showinfo(f"Acción completada", f"El {obj_type} fue copiado con éxito")
            self.destroy()

        self.parent.updateDiskState()
        self.parent.reloadFileSystem()

    def __copy_VirtualToVirtual(self):

        if self.selected_obj is None:
            messagebox.showerror("No existe ningún objeto seleccionado", "La ruta ingresada no corresponde a ningún objeto dentro del file system")
            return

        path_origin, path_destiny = self.__getInputPaths()
        directory_destiny: Directory = self.parent.fileSystem.navigateToDirectory( path_destiny )

        obj_type: str = ""
        copy_result: bool = True

        if directory_destiny is None:
            messagebox.showerror("Directorio destino no existe", "El directorio de destino no pudo ser encontrado, por favor ingrese una ruta válida")
            return

        if self.isFile:
            obj_type = "Archivo"
            file_name = self.selected_obj.name
            file_extension = self.selected_obj.extension
            file_content = self.selected_obj.content

            if not self.parent.isUniqueInDestinyDir( f"{file_name}.{file_extension}", "File", path_destiny ):
                answer = messagebox.askyesno("Archivo existe en el destino", "Existe un archivo con el mismo nombre en el destino. ¿Desea sobreescribir su contenido?")
                if answer:
                    selected_file: File = self.parent.getFileObj( f"{file_name}.{file_extension}", path_destiny )

                    oldSectorsList = self.parent.fileSystem.fat.getFileSectors( selected_file.fat_index )
                    newSectorsList = self.parent.fileSystem.disk.writeToDisk( file_content, oldSectorsList )
                    if (newSectorsList == []):
                        return
                    self.parent.fileSystem.fat.freeFATEntries( selected_file.fat_index )
                    newStartingIndex = self.parent.fileSystem.fat.assingSectorList(newSectorsList)

                    selected_file.modifyContent( file_name, file_extension, file_content )
                    selected_file.assignSectors( newStartingIndex )
                    copy_result = True
                else:
                    copy_result = False
            else:
                self.parent.fileSystem.createFile( file_name, file_extension, file_content, directory_destiny )
                copy_result = True
        else:
            obj_type = "Directorio"
            dir_name = self.selected_obj.name

            if not self.parent.isUniqueInDestinyDir( dir_name, "Directory", path_destiny ):
                answer = messagebox.askyesno("Directorio existe en el destino", "Existe un directorio con el mismo nombre en el destino. ¿Desea sobreescribir su contenido?")
                if answer:
                    selected_dir: Directory = self.parent.getDirObj( dir_name, path_destiny )
                    self.parent.fileSystem.clearDirectory (selected_dir)

                    directory_destiny.directories.pop( dir_name )
                else:
                    copy_result = False
                    return

            # Create the directory in its destiny
            directory_destiny = self.parent.fileSystem.createDirectory( dir_name, directory_destiny )

            # Copy its content recursively
            self.__copy_DirectoryContentRecursively(self.selected_obj, directory_destiny)
            copy_result = True

        self.parent.updateDiskState()

        if copy_result:
            messagebox.showinfo(f"Acción completada", f"El {obj_type} fue copiado con éxito")
            self.destroy()