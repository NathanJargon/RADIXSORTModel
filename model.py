import tkinter as tk
from tkinter import messagebox, simpledialog
import numpy as np
import scipy.stats as stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
from functions import (
    calculate_correlation,
    calculate_regression,
    calculate_anova,
    calculate_mse,
    sort_data,
    initialize_blank_graph
)

def generate_random_data(entry):
    num_points = simpledialog.askinteger("Input", "How many data points?", minvalue=1)
    if num_points:
        random_data = np.random.rand(num_points)
        entry.delete("1.0", tk.END)
        entry.insert(tk.END, ' '.join(map(str, random_data)))

root = tk.Tk()
root.title("Data Analysis Tool")
root.geometry("1200x900")

input_frame = tk.Frame(root)
input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

x_labels = []
x_entries = []
generate_buttons = []

x_data_frame = tk.Frame(input_frame)
x_data_frame.pack(side=tk.TOP, fill=tk.X)

def add_x_entry():
    if len(x_entries) < 4:
        new_x_label = tk.Label(x_data_frame, text=f"X Data {len(x_entries) + 1}:")
        new_x_label.pack(side=tk.TOP, anchor='w', pady=(10, 0))
        new_x_entry = tk.Text(x_data_frame, height=3, width=50)
        new_x_entry.pack(side=tk.TOP, anchor='w', pady=(0, 10))
        generate_button = tk.Button(x_data_frame, text="Generate", command=lambda e=new_x_entry: generate_random_data(e))
        generate_button.pack(side=tk.TOP, anchor='w', pady=(0, 10))
        
        x_labels.append(new_x_label)
        x_entries.append(new_x_entry)
        generate_buttons.append(generate_button)

def remove_x_entry():
    if len(x_entries) > 1:
        last_entry = x_entries.pop()
        last_entry.destroy()
        last_label = x_labels.pop()
        last_label.destroy()
        last_button = generate_buttons.pop()
        last_button.destroy()

tk.Label(x_data_frame, text="X Data 1:").pack(side=tk.TOP, anchor='w', pady=(10, 0))
x_entry = tk.Text(x_data_frame, height=3, width=50)
x_entry.pack(side=tk.TOP, anchor='w', pady=(0, 10))
x_entries.append(x_entry)
generate_button = tk.Button(x_data_frame, text="Generate", command=lambda e=x_entry: generate_random_data(e))
generate_button.pack(side=tk.TOP, anchor='w', pady=(0, 5))
generate_buttons.append(generate_button)

add_button_frame = tk.Frame(input_frame)
add_button_frame.pack(pady=10)

tk.Button(add_button_frame, text="Add X Data", command=add_x_entry).pack(side=tk.LEFT, padx=5)
tk.Button(add_button_frame, text="Remove X Data", command=remove_x_entry).pack(side=tk.LEFT, padx=5)

tk.Label(input_frame, text="Y Data:").pack(side=tk.TOP, anchor='w', pady=(10, 0))
y_entry = tk.Text(input_frame, height=3, width=50)
y_entry.pack(side=tk.TOP, anchor='w', pady=(0, 10))
generate_button_y = tk.Button(input_frame, text="Generate", command=lambda e=y_entry: generate_random_data(e))
generate_button_y.pack(side=tk.TOP, anchor='w', pady=(0, 10))

result_label = tk.Label(input_frame, text="Results will be shown here", wraplength=400, relief="solid", borderwidth=2)
result_label.pack(pady=(20, 10), padx=10)

button_frame = tk.Frame(input_frame)
button_frame.pack(side=tk.BOTTOM, pady=10)

tk.Button(button_frame, text="Correlation", command=lambda: calculate_correlation(x_entries, y_entry, result_label, graph_frame)).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Regression", command=lambda: calculate_regression(x_entries, y_entry, result_label, graph_frame)).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="ANOVA", command=lambda: calculate_anova(x_entries, result_label)).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="MSE", command=lambda: calculate_mse(x_entries, y_entry, result_label)).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Radix Sort Data", command=lambda: sort_data(x_entries, result_label)).pack(side=tk.LEFT, padx=5)

graph_frame = tk.Frame(root)
graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

initialize_blank_graph(graph_frame)

root.mainloop()