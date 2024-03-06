import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import LinearSegmentedColormap
import ternary
from quaternary import quaternary
import re

class PlotApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GeoPlotter")
        self.geometry("1000x700")
        
        self.data = None
        self.labels = []
        self.start_color = '#0000FF' 
        self.end_color = '#FF0000' 
        self.canvas = None
        self.plot_title = "Plot Title" 

        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.TOP, fill=tk.X)

        self.load_button = tk.Button(button_frame, text="Load CSV", command=self.load_csv)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(button_frame, text="Save Graph", command=self.save_graph)
        self.save_button.pack(side=tk.LEFT, padx=5)

        tk.Label(button_frame, text=" " * 20).pack(side=tk.LEFT, expand=True)

        self.rename_labels_button = tk.Button(button_frame, text="Rename Labels", command=self.rename_labels)
        self.rename_labels_button.pack(side=tk.RIGHT, padx=5)

        self.rename_plot_button = tk.Button(button_frame, text="Rename Plot", command=self.rename_plot)
        self.rename_plot_button.pack(side=tk.RIGHT, padx=5)

        self.end_color_button = tk.Button(button_frame, text="Color 2", command=self.choose_end_color)
        self.end_color_button.pack(side=tk.RIGHT, padx=5)

        self.start_color_button = tk.Button(button_frame, text="Color 1", command=self.choose_start_color)
        self.start_color_button.pack(side=tk.RIGHT, padx=5)

    def format_label(self, label):
        return re.sub(r'(\d+)', r'$_{\1}$', label)

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        try:
            self.data = pd.read_csv(file_path)
            num_cols = len(self.data.columns)
            if num_cols < 3 or num_cols > 4:
                messagebox.showerror("Error", "Data must be ternary or quaternary.")
                return
            
            self.labels = self.data.columns.tolist()
            self.plot_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")

    def plot_data(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        num_components = len(self.data.columns)
        self.fig = plt.Figure(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        
        if num_components == 3:
            scale = 100
            figure, tax = ternary.figure(scale=scale, ax=self.fig.add_subplot(111))
            tax.set_title(self.plot_title, fontsize=20)
            tax.boundary(linewidth=2.0)
            tax.gridlines(color="blue", multiple=10)
            tax.clear_matplotlib_ticks()
            tax.ticks(axis='lbr', linewidth=1, multiple=20)
            
            formatted_labels = [self.format_label(label) for label in self.labels]
            tax.left_axis_label(formatted_labels[0], fontsize=10)
            tax.right_axis_label(formatted_labels[1], fontsize=10)
            tax.bottom_axis_label(formatted_labels[2], fontsize=10)
            
            normalized_data = self.data.div(self.data.sum(axis=1), axis=0) * scale
            max_values = normalized_data.max(axis=1)
           
            adjusted_values = (max_values - 33.333) / (66.667 - 33.333)
            custom_cmap = LinearSegmentedColormap.from_list("custom_cmap", [self.start_color, self.end_color])
            colors = custom_cmap(np.clip(adjusted_values, 0, 1))
            
            for point, color in zip(normalized_data.values, colors):
                tax.scatter([point], marker='o', color=[color])
        else:
           
            normalized_data = self.data.to_numpy()
            normalized_data /= normalized_data.sum(axis=1)[:, np.newaxis]
            normalized_data *= 100
            max_values = normalized_data.max(axis=1)
            adjusted_values = (max_values - 25) / (100 - 25)
            custom_cmap = LinearSegmentedColormap.from_list("custom_cmap", [self.start_color, self.end_color])
            colors = custom_cmap(np.clip(adjusted_values, 0, 1))

            quat = quaternary(self.fig)
            quat.set_grid()
            
            formatted_labels = [self.format_label(label) for label in self.labels]
            quat.set_label1(formatted_labels[0])
            quat.set_label2(formatted_labels[1])
            quat.set_label3(formatted_labels[2])
            quat.set_label4(formatted_labels[3])
            
            self.fig.suptitle(self.plot_title,fontsize=20)

            quat.scatter(normalized_data[:, 0], normalized_data[:, 1], normalized_data[:, 2], facecolor=colors, marker='o')

        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas.draw()

    def choose_start_color(self):
        color_code = colorchooser.askcolor(title="Choose Start Color")[1]
        if color_code:
            self.start_color = color_code
            if self.data is not None:
                self.plot_data()

    def choose_end_color(self):
        color_code = colorchooser.askcolor(title="Choose End Color")[1]
        if color_code:
            self.end_color = color_code
            if self.data is not None:
                self.plot_data()

    def rename_labels(self):
        def update_labels():
            new_labels = [entry.get() for entry in entries]
            if len(self.labels) == 4 and len(new_labels) == 3: 
                new_labels.append('') 
            if not all(new_labels): 
                messagebox.showerror("Error", "All labels must be provided.")
                return
            self.labels = new_labels
            if self.data is not None:
                self.plot_data()
            rename_window.destroy()

        rename_window = tk.Toplevel(self)
        entries = []
        for i, label in enumerate(self.labels):
            tk.Label(rename_window, text=f"Label {i + 1}:").pack()
            entry = tk.Entry(rename_window)
            entry.insert(0, label)
            entry.pack()
            entries.append(entry)

        submit_button = tk.Button(rename_window, text="Update Labels", command=update_labels)
        submit_button.pack()

    def rename_plot(self):
        def update_title():
            new_title = title_entry.get()
            if not new_title.strip():
                messagebox.showerror("Error", "The plot title cannot be empty.")
                return
            self.plot_title = new_title.strip()
            if self.data is not None:
                self.plot_data() 
            rename_window.destroy()

        rename_window = tk.Toplevel(self)
        tk.Label(rename_window, text="Enter new plot title:").pack()
        
        title_entry = tk.Entry(rename_window)
        title_entry.pack(padx=5, pady=5)
        title_entry.insert(0, self.plot_title) 

        submit_button = tk.Button(rename_window, text="Update Title", command=update_title)
        submit_button.pack(pady=5)

    def save_graph(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPG files", "*.jpg")])
        if file_path:
            self.fig.savefig(file_path)

app = PlotApp()
app.mainloop()
