import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
from zipfile import ZipFile
import os, shutil, configparser, sqlite3
from tkinter import messagebox

class Viewer:
    def __init__(self, master, temp_manga=""):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.manga = 0
        self.path = "./data/cache"
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
        self.button_list = []
        self.file_list = []
        self.sql = sqlite3.connect('./data/sql/ComicTool.sqlite')
        self.master.title("ComicTools")
        self.menuBar = tk.Menu(self.master)

        self.x = None
        self.y = None

        self.display()

    def display(self):
        file = tk.Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label='File', menu=file)
        file.add_command(label='Add New Folder', command=None)
        file.add_command(label='List Current Folder(s)', command=None)
        file.add_command(label='Change hash folder', command=None)
        file.add_separator()
        file.add_command(label='Save & Exit', command=lambda: self.on_closing())

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
        self.master.update()
        h, w = self.master.winfo_height(), self.master.winfo_width()

        frame_top = tk.Frame(self.master, width=w, height=h*0.05, bg="#154e72")
        frame_left = tk.Frame(self.master, width=w * 0.15, height=h*0.85, bg="#3399ff")
        frame_right = tk.Frame(self.master, width=w * 0.85, height=h*0.85, bg="#9dc8e3")
        frame_bottom = tk.Frame(self.master, width=w, height=h*0.1, bg="#154e72")

        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        frame_top.pack(side='top', expand=True, fill='both')
        frame_bottom.pack(side='bottom', expand=True, fill='both')
        frame_left.pack(side='left', expand=True, fill='both')
        frame_right.pack(side='right', expand=True, fill='both')

        frame_top.grid_propagate(0)
        frame_bottom.grid_propagate(0)
        frame_left.grid_propagate(0)
        frame_right.grid_propagate(0)

        # Adding to right size of top bar
        # Add closing icon
        logo_img = Image.open(r'./source/close.png')
        logo = ImageTk.PhotoImage(logo_img.resize((int(h * 0.05), int(h * 0.05))))

        self.close = tk.Button(self.master, image=logo, command=lambda: self.on_closing())
        self.close.image = logo
        self.close.pack(in_=frame_top, side="right", fill="y")

        # Add dragging icon
        move_logo_img = Image.open(r'./source/move.png')
        move_logo = ImageTk.PhotoImage(move_logo_img.resize((int(h*0.05), int(h*0.05))))

        self.grip = tk.Label(self.master, image=move_logo)
        self.grip.image = move_logo
        self.grip.pack(in_=frame_top, side="right", fill="y")

        self.grip.bind("<ButtonPress-1>", self.start_move)
        self.grip.bind("<ButtonRelease-1>", self.stop_move)
        self.grip.bind("<B1-Motion>", self.do_move)

        for i in range(4):
            for j in range(4):
                but = tk.Button(self.master, text="test"+str(i)+','+str(j))
                but.grid(in_=frame_right, column=i, row=j, sticky="NSEW")
                self.button_list.append(but)

        for x in range(4):
            tk.Grid.columnconfigure(frame_right, x, weight=1)

        for y in range(4):
            tk.Grid.rowconfigure(frame_right, y, weight=1)

        print(self.button_list)


    def thumbnails(self):
        thumbnail_ratio = (64, 100)
        for filename in os.listdir('./data/cache'):
            file_path = os.path.join('./data/cache', filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed deletion')


        if len(temp_path) == 0:
            print('Invalid path: '+temp_path+' Skipped')

        if os.path.isfile(temp_path):
            book = ZipFile(temp_path, 'r')
            book.extractall('./data/cache')
            book.close()

        def loadBook(self):
            self.newWindow = tk.Toplevel(self.master)
            self.newWindow.minsize(width=800, height=1080)
            self.app = Viewer(self.newWindow)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.master.winfo_x() + deltax
        y = self.master.winfo_y() + deltay
        self.master.geometry(f"+{x}+{y}")

    def on_closing(self):
        self.sql.close()
        self.master.destroy()

def get_config(section, parameter):
    conf = configparser.ConfigParser()

    if os.path.isfile(r"./data/settings.ini"):
        conf.read(r"./data/settings.ini")

    else:
        conf['Default'] = {'width': '1200',
                           'height': '1080'}

        with open('./data/settings.ini', 'w') as configfile:
            conf.write(configfile)

    return conf.get(section, parameter)

def set_config(section, parameter):
    conf = configparser.ConfigParser()
    conf.read(r"./data/settings.ini")

    conf[section] = parameter

    with open('./data/settings.ini', 'w') as configfile:
        conf.write(configfile)



def main():
    if not os.path.exists('./data'):
        os.mkdir('data')

    if not os.path.exists('./data/sql'):
        os.mkdir('data/sql')

    if not os.path.exists('./data/cache'):
        os.mkdir('data/cache')

    root = tk.Tk()
    conf_width, conf_height = get_config('Default', 'width'), get_config('Default', 'height')

    root.minsize(width=conf_width, height=conf_height)
    root.maxsize(width=conf_width, height=conf_height)
    root.overrideredirect(True)
    app = DatabaseView(root)
    root.mainloop()


if __name__ == '__main__':
    main()
