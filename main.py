import tkinter as tk
from tkinter import ttk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import style

from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator, MultipleLocator

import math

import statistics

import numpy as np

import data_actor

import webbrowser



LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

style.use("ggplot")

f = plt.figure()

a = f.add_subplot(111)


def update_graph(data):
    global autoscale
    autoscale = 0
    actor_name, score_data = data
    a.clear()
    x, y, title_array, url_array, year_array, mean, med = organize_data(score_data)
    mean, med = round(mean, 1), round(med, 1)

    a.scatter(x, y, color="black")
    line_of_best_fit(x, y)
    f.suptitle(actor_name, fontsize=16, fontweight='bold')

    a.set_title("Average score: "+ str(mean) + "%       Median score: " + str(med) + "%", fontsize=10)
    axis_settings(a, y)
    global annot_list
    annot_list = []

    f.canvas.draw()


def axis_settings(subplot, score_array):
    subplot.xaxis.set_major_locator(MaxNLocator(integer=True))
    subplot.xaxis.set_minor_locator(MultipleLocator(1))
    subplot.yaxis.set_major_locator(MultipleLocator(10))
    subplot.yaxis.set_minor_locator(MultipleLocator(5))
    subplot.set_xlabel("Movie Number")
    subplot.set_ylabel("Tomatometer %")
    # plt.subplots_adjust(right=0.8)

    int_score_array = [int(i) for i in score_array]
    max_y = int(math.ceil(float(max(int_score_array))/10)*10)
    min_y = int(math.floor(float(min(int_score_array))/10)*10)
    if max(int_score_array) % 10 == 0:
        max_y += 4
    if min(int_score_array) % 10 == 0:
        min_y -= 4
    subplot.set_ylim([min_y, max_y])


def line_of_best_fit(x, y):
    # Simply uses numpy to get line of best fit
    m, b = np.polyfit(np.array(x, dtype=float), np.array(y, dtype=float), 1)
    x2 = np.linspace(1, len(x))
    a.plot(x2, m*x2+b, color="red")


def popup(msg):
    # Displays pop up with given message.
    popup = tk.Tk()
    popup.wm_title("Incorrect Input")
    label = ttk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    b1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    b1.pack()
    popup.mainloop()


def fetch_actor_data(entry):
    actor_name = entry.get()
    actor_page = data_actor.get_actor_page(actor_name)
    score_data = data_actor.web_scrape(actor_page)
    if not score_data:
        popup("Actor/director not found on Rotten Tomatoes! Please enter a valid name.")
    return score_data


def change_page(self, controller, entry):
    global score_data
    score_data = fetch_actor_data(entry)
    if not score_data:
        popup("Actor/director not found on Rotten Tomatoes! Please enter a valid name.")
    else:
        update_graph(score_data)
        controller.show_frame(ActorGraphPage)


def organize_data(score_data):
    length = len(score_data)
    global movie_number, score_array, title_array, url_array, year_array
    movie_number = [n+1 for n in range(length)]
    score_array = [int(movie[0]) for movie in score_data]

    title_array = [movie[1] for movie in score_data]
    url_array = ["https://www.rottentomatoes.com" + movie[2] for movie in score_data]
    year_array = [movie[3] for movie in score_data]
    mean, med = statistics.mean(score_array), statistics.median(score_array)

    return movie_number, score_array, title_array, url_array, year_array, mean, med


def update_annotation(event):
    # deletes all previous annotations
    if annot_list:
        for ann in annot_list:
            try:
                ann.remove()
            except ValueError:
                pass

    if not event.xdata or not event.ydata:
        pass
    # checks if cursor is within a certain plot to display an annotation
    else:
        for i in range(len(movie_number)):
            if abs(event.xdata - movie_number[i]) <= .23*len(movie_number)/26 and abs(event.ydata - int(score_array[i])) <= 1.2:
                txt = title_array[i]+"\n"+"Score: "+str(score_array[i])+"%"+"\n"+year_array[i]
                bbox_props = dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=1, alpha=0.75)
                x_place, y_place = scale_annotation(event, a, title_array[i], len(movie_number))
                annot = a.annotate(txt, (movie_number[i], int(score_array[i])), xytext=(x_place, y_place),
                                   visible=True, bbox=bbox_props, fontsize=10)

                annot_list.append(annot)
    f.canvas.draw()


def scale_annotation(event, subplot, movie_title, movie_count):
    add_chars = 0
    x_min, x_max = subplot.get_xlim()
    y_min, y_max = subplot.get_ylim()
    range = y_max - y_min

    if len(movie_title) > 10:
        add_chars = len(movie_title) - 10
    x_place = min(event.xdata + .28*movie_count/26, x_max-3.75*movie_count/26-.33*movie_count/26*add_chars)
    y_place = min(event.ydata + 2.5, y_max-13.75*range/104)

    return x_place, y_place


def get_link(event):
    # if click event happens within certain plot, opens associated URL
    if not event.xdata or not event.ydata:
        pass
    else:
        for i in range(len(movie_number)):
            if abs(event.xdata - movie_number[i]) <= .23 and abs(event.ydata - int(score_array[i])) <= 1.2:
                webbrowser.open(url_array[i])


class RT(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.shared_data = []

        tk.Tk.iconbitmap(self, default="tomato-icon2.ico")
        tk.Tk.wm_title(self, "Tomatometer Grapher")
        container = ttk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        tk.Tk.config(self, menu=menubar)

        for F in (StartPage, ActorSearchPage, ActorGraphPage, FranchiseSearchPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def get_page(self, frame):
        return self.frames[frame]


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text=("""\nTomatometer Grapher"""), font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        label2 = ttk.Label(self, text=("""The Tomatometer Grapher is a visualization tool, that graphs the 
overall Rotten Tomatoes score of a given actor/actress or director."""), font=NORM_FONT)
        label2.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="View Graph of Actor/Director",
                             command=lambda: controller.show_frame(ActorSearchPage))
        button1.pack(pady=5, padx=10)

        button2 = ttk.Button(self, text="View Graph of Franchises (Coming Soon)",
                            command=lambda: controller.show_frame(FranchiseSearchPage))
        button2.pack(pady=5, padx=10)

        button3 = ttk.Button(self, text="Exit",
                            command=quit)
        button3.pack(pady=5, padx=10)


class ActorSearchPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="\nSearch for an Actor/Director", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        label2 = ttk.Label(self, text="""It is required to spell the name as it is expressed on Rotten Tomatoes.""", font=NORM_FONT)
        label2.pack()

        entry = ttk.Entry(self, width=30)
        entry.pack(pady=10, padx=10)
        entry.bind("<Return>", (lambda event: change_page(self, controller, entry)))

        button1 = ttk.Button(self, text="Search Actor/Director",
                             command=lambda: change_page(self, controller, entry))
        button1.pack(pady=5, padx=10)

        button2 = ttk.Button(self, text="Go Back to Main Page",
                             command=lambda: controller.show_frame(StartPage))
        button2.pack(pady=5, padx=10)


class ActorGraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.createGraph()

        button1 = ttk.Button(self, text="Back",
                             command=lambda: controller.show_frame(ActorSearchPage))
        button1.pack()

    def createGraph(self):
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        canvas.mpl_connect('button_press_event', get_link)
        canvas.mpl_connect('motion_notify_event', update_annotation)


class FranchiseSearchPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        label = ttk.Label(self, text="Search for a Franchise", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        label2 = ttk.Label(self, text=("""The following franchises can be searched:"""), font=NORM_FONT)
        label2.pack()

        listbox = tk.Listbox(self)
        listbox.pack()

        for item in ["Star Wars", "Lord of the Rings", "Harry Potter", "X-Men", "Marvel", "DC", "Fast and Furious","Batman","Pixar"]:
            listbox.insert(0, item)

        button1 = ttk.Button(self, text="Search Franchise",
                            command=lambda: popup("This feature is not available at the time"))
        button1.pack(pady=10, padx=10)

        button2 = ttk.Button(self, text="Go Back to Main Page",
                             command=lambda: controller.show_frame(StartPage))
        button2.pack()


app = RT()
app.geometry("800x550")
app.mainloop()