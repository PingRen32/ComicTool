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
        for filename in os.listdir('./data/cache'):
            file_path = os.path.join('./data/cache', filename)
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
        self.path = "./data/cache"
        self.images = []
        self.cur_site = 0

        self.master.title("ComicTools")
        self.menuBar = tk.Menu(self.master)

        file = tk.Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label='File', menu=file)
        file.add_command(label='Add New Folder', command=None)
        file.add_command(label='List Current Folder(s)', command=None)
        file.add_command(label='Change hash folder', command=None)
        file.add_separator()
        file.add_command(label='Exit', command=lambda: self.master.destroy())

        # Adding Edit
        edit = tk.Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label='Tag', menu=edit)
        edit.add_command(label='Add Tag', command=None)
        edit.add_command(label='Remove Tag', command=None)
        edit.add_command(label='File Tag', command=None)
        edit.add_command(label='File Un-Tag', command=None)
        edit.add_separator()
        edit.add_command(label='Find...', command=None)
        edit.add_command(label='Find again', command=None)

        # Adding Tools Menu
        tools = tk.Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label='Tools', menu=tools)
        tools.add_command(label='Load hash/Tag', command=None)
        tools.add_command(label='Demo', command=None)
        tools.add_separator()
        tools.add_command(label='About Tk', command=None)

        # Adding Help Menu
        help = tk.Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label='Help', menu=help)
        help.add_command(label='Tk Help', command=None)
        help.add_command(label='Demo', command=None)
        help.add_separator()
        help.add_command(label='About Tk', command=None)


        self.master.config(menu=self.menuBar)

    def thumbnails(self):
        thumbnail_ratio = (64, 100)

    def loadBook(self):
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.minsize(width=800, height=1200)
        self.app = Viewer(self.newWindow)



def main():
    if not os.path.isdir('./data'):
        os.system("mkdir data")

    if not os.path.isdir('./data/hash'):
        os.system(r"mkdir ./data/hash")

    if not os.path.isdir('./data/cache'):
        os.system(r"mkdir ./data/cache")

    root = tk.Tk()
    root.minsize(width=1600, height=1200)
    app = DatabaseView(root)
    root.mainloop()

if __name__ == '__main__':
    main()
