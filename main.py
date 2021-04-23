import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
from zipfile import ZipFile
import os, shutil

class Viewer:
    def __init__(self, master, temp_manga=""):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.manga = 0
        self.path = "./cache"
        self.images = []
        self.cur_page = 0
        self.frame.panel = tk.Label(self.frame)
        self.frame.pack()
        self.temp_manga = temp_manga

        self.btn_decrease = tk.Button(self.frame, text="-")
        self.lbl_value = tk.Label(self.frame, text="0")
        self.btn_increase = tk.Button(self.frame, text="+")

        self.btn_increase = tk.Button(self.frame, text="+", command=lambda: self.loadImage(1))
        self.btn_decrease = tk.Button(self.frame, text="-", command=lambda: self.loadImage(-1))

        self.master.bind("<Left>", lambda i: self.loadImage(-1))
        self.master.bind("<Right>", lambda i: self.loadImage(1))
        self.master.bind("<Up>", lambda i: self.loadImage(-1))
        self.master.bind("<Down>", lambda i: self.loadImage(1))
        self.master.bind("<Prior>", lambda i: self.loadImage(-1))
        self.master.bind("<Next>", lambda i: self.loadImage(1))

        self.lbl_value.pack(side=tk.BOTTOM, fill="none")
        self.btn_decrease.pack(side=tk.LEFT, fill="y")
        self.btn_increase.pack(side=tk.RIGHT, fill="y")

        self.loadBook(self.temp_manga)

    def loadBook(self, temp_manga=""):
        self.clearCache()

        if len(temp_manga) == 0:
            temp_manga = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file", filetypes=(("Manga or Comic Files", ".cbr .cbz"), ("all files", "*.*")))

        if os.path.isfile(temp_manga):
            book = ZipFile(temp_manga, 'r')
            book.extractall(self.path)
            book.close()

            for file in os.scandir(self.path):
                self.images.append(file.name)

            self.manga = temp_manga
            self.initImage()
            self.frame.winfo_toplevel().title(os.path.basename(self.manga))

        else:
            if self.manga:
                book = ZipFile(self.manga, 'r')
                book.extractall(self.path)
                book.close()

                for file in os.scandir(self.path):
                    self.images.append(file.name)

                self.initImage()
                self.frame.winfo_toplevel().title(os.path.basename(self.manga))

            else:
                self.loadBook()

    def printFile(self):
        print(self.manga)

    def loadImage(self, num):
        self.cur_page = self.cur_page + num

        if self.cur_page < 0:
            self.cur_page = len(self.images) - 1

        if self.cur_page >= len(self.images):
            self.cur_page = 0

        w, h = self.master.winfo_width()*0.94, self.master.winfo_height()*0.94
        tmp_img = Image.open(os.path.join("cache", self.images[self.cur_page]))

        if w/h >= tmp_img.width/tmp_img.height:
            tmp_img = tmp_img.resize((round(tmp_img.width/tmp_img.height * h), round(h)), Image.ANTIALIAS)
        else:
            tmp_img = tmp_img.resize((round(w), round(tmp_img.height/tmp_img.width * w)), Image.ANTIALIAS)

        img = ImageTk.PhotoImage(tmp_img)

        self.lbl_value["text"] = f"{self.cur_page}" + "/" + f"{len(self.images)}"

        self.frame.panel.configure(image=img)
        self.frame.panel.image = img
        self.frame.panel.pack(side="bottom", fill="both", expand="yes")

    def initImage(self):
        tmp_img = Image.open(os.path.join("cache", self.images[self.cur_page]))
        img = ImageTk.PhotoImage(tmp_img)

        self.frame.panel.configure(image=img)
        self.frame.panel.image = img
        self.frame.panel.pack(side="bottom", fill="both", expand="yes")

        self.loadImage(0)
        self.master.lift()

    def clearCache(self):
        for filename in os.listdir('./cache'):
            file_path = os.path.join('./cache', filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def close_windows(self):
        self.master.destroy()


class DatabaseView:
    def __init__(self, master):
        self.master = master
        self.manga = 0
        self.path = "./cache"
        self.images = []
        self.cur_site = 0

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.master.title("ComicTools")
        self.menuBar = tk.Menu(self.master)

        file = tk.Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label='File', menu=file)
        file.add_command(label='New File', command=None)
        file.add_command(label='Open...', command=None)
        file.add_command(label='Save', command=None)
        file.add_separator()
        file.add_command(label='Exit', command=self.master.destroy)

        # Adding Edit Menu and commands
        edit = tk.Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label='Edit', menu=edit)
        edit.add_command(label='Cut', command=None)
        edit.add_command(label='Copy', command=None)
        edit.add_command(label='Paste', command=None)
        edit.add_command(label='Select All', command=None)
        edit.add_separator()
        edit.add_command(label='Find...', command=None)
        edit.add_command(label='Find again', command=None)

        # Adding Help Menu
        help_ = tk.Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label='Help', menu=help_)
        help_.add_command(label='Tk Help', command=None)
        help_.add_command(label='Demo', command=None)
        help_.add_separator()
        help_.add_command(label='About Tk', command=None)

        self.load_button = tk.Button(self.frame, text="Load E-Book", command=self.loadBook)
        self.load_button.pack(side=tk.TOP)

        self.master.config(menu=self.menuBar)

    def thumbnails(self):
        thumbnail_ratio = (64, 100)

    def loadBook(self):
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.minsize(self.master.winfo_width(), self.master.winfo_height())
        self.app = Viewer(self.newWindow)



def main():
    if not os.path.isdir('./cache'):
        os.system("mkdir cache")

    root = tk.Tk()
    root.minsize(width=800, height=1200)
    app = DatabaseView(root)
    root.mainloop()

if __name__ == '__main__':
    main()
