from tkinter.ttk import Frame, Label, Button
from tkinter import Tk, filedialog, Text, Menu, Toplevel, messagebox, PhotoImage
from tkinter.constants import WORD, FLAT, END, CENTER
import sys
import os

__author__ = "Sergei Shekin"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Sergei Shekin"
__email__ = "shekin.sergey@yandex.com"

basedir = os.path.abspath(os.path.dirname(__file__))


def center(window, dvx: float = 2.5, dvy: float = 2.5) -> None:
    """Opening window on center of the screen

    Args:
        dvx ():
        dvy ():
        window (tkTk): parent window of tk.Tk application
    """
    x = (window.winfo_screenwidth() - window.winfo_reqwidth()) / dvx
    y = (window.winfo_screenheight() - window.winfo_reqheight()) / dvy
    window.wm_geometry("+%d+%d" % (x, y))


def warning_box(text) -> None:
    """Warning window with Error message

    Args:
        text ([type]): Text provided to the message box.
    """
    messagebox.showinfo(title='Message', message=text)


class About(Toplevel):
    """Window for "About" information

    Args:
        Toplevel ([type]): child of main class window
    """

    def __init__(self, parent) -> None:
        text = '''
        Especially for my Polish comrade. 
        The principle of operation is simple: 
        open the source file and save it in CSV format
        '''
        design = f'Created by {__maintainer__}\nemail: {__email__}'
        super().__init__(parent)
        center(self, dvx=2.3, dvy=2.3)
        self.label = Label(self, text=text, padding=15, font=('Arial', 10, 'normal'), width=70, wraplength=500)
        self.design = Label(self, text=design, justify='center', font=('Arial', 8, 'normal'))
        self.button = Button(self, text="Close", command=self.destroy)
        self.title('About')
        self.attributes('-topmost', True)  # On top over all windows

        self.label.pack(side='top', fill='y')
        self.design.pack(side='top', fill='y')
        self.button.pack(fill='both', side='bottom')


class CarisConverter(Tk):
    """Main class for main window

    Args:
        Tk ([type]): parent
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        icon = os.path.join(basedir, 'img', 'icon.png')
        self.iconphoto(True, PhotoImage(file=icon))
        self.title('Waldi\'s Caris lines converter')
        center(self)
        self.resizable(width=False, height=False)
        self.menu_ui()
        # self.geometry('900x200')
        for index in range(11):
            self.grid_rowconfigure(index, weight=1)
            self.grid_columnconfigure(index, weight=0)

        self.source_text = ''
        self.new_csv_text = []

        self.frameBottom = Frame(self)
        self.but_open_file = Button(self, text='Open', command=self.open_file)
        self.but_open_file.grid(row=0, column=0, columnspan=6, sticky='WE')
        self.saveGen = Button(self, text='CSV', command=self.save_csv)
        self.saveGen.grid(row=0, column=6, columnspan=6, sticky='WE')

        self.showFrame = Frame(self)
        self.showFrame.grid(row=1, rowspan=5, column=0, columnspan=12, sticky='NSWE')
        self.textFile = Text(self.showFrame, relief=FLAT, height=8, width=80, font=('Arial', 8, 'normal'), wrap=WORD)
        self.textFile.grid(row=0, column=0, columnspan=12, rowspan=5, sticky='NSEW')
        self.show_in_text_field(self.source_text)

        self.butExit = Button(self, text='Exit', command=self.exit_app)
        self.butExit.grid(row=10, column=0, columnspan=12, sticky='WE')

    def menu_ui(self):
        main_menu = Menu(self)
        self.config(menu=main_menu)
        file_menu = Menu(main_menu, tearoff=0)
        file_menu.add_command(label='Open', command=self.open_file)
        file_menu.add_command(label='Exit', command=self.exit_app)

        main_menu.add_cascade(label='File', menu=file_menu)
        main_menu.add_command(label='About', command=lambda: About(self))

    def open_file(self) -> (str, None):
        try:
            files = (
                ('TXT files', '*.txt'),
                ('All files', '*.*'),
            )
            file = os.path.normpath(filedialog.askopenfilename(filetypes=files, title='Open source file'))
            with open(file, 'r', encoding='utf-8') as f:
                text = f.read()
            self.source_text = text
            self.new_csv_text = self.generate_csv(text)
            self.show_in_text_field(text=text)
        except Exception as e:
            warning_box(text=f'Error: file not defined')

    def show_in_text_field(self, text: str = '', new_text=None):
        self.textFile.delete(0.1, END)
        if new_text:
            for line in text[::-1]:
                self.textFile.insert(0.1, line + "\n")
        elif text:
            self.textFile.insert(0.1, text)
        else:
            pass

    def generate_csv(self, text) -> list:
        """
        Генерирует и возвращает новый текст CSV
        :param text: Исходный текст
        :type text: str
        :return: строки текста
        :rtype: list
        """
        count = 1
        text_lines = []
        for line in text.split('\n'):
            line = line.replace(' ', '').replace(',', '').split('(m)')
            box = str(count) + "\n" + ';'.join(line[:2]) + "\n" + ';'.join(line[2:4]) + "\n"
            text_lines.append(box)
            count += 1
        self.show_in_text_field(new_text=text_lines)
        return text_lines

    def save_csv(self):
        if self.new_csv_text:
            try:
                files = (
                    ('CSV files', '*.csv'),
                    ('TXT files', '*.txt'),
                    ('All files', '*.*'),
                )
                file = os.path.normpath(
                    filedialog.asksaveasfilename(confirmoverwrite=True, filetypes=files, defaultextension='.csv',
                                                 title='Save as', initialfile='output'))
                with open(file, 'w+', encoding='utf-8') as f:
                    for line in self.new_csv_text:
                        f.write(line)
                if sys.platform == "win32":
                    if messagebox.askyesno(message='Open the saved file?'):
                        os.startfile(file)
                    else:
                        pass
            except Exception as e:
                warning_box(text=f'Not saved\n{e}')
        else:
            warning_box(text='Open file first')

    def start_app(self):
        self.mainloop()

    def exit_app(self):
        self.destroy()
        sys.exit(0)


if __name__ == "__main__":
    a = CarisConverter()
    a.start_app()
