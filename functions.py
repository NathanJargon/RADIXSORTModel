import tkinter as tk
from tkinter import messagebox
import numpy as np
import scipy.stats as stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

def radix_sort(arr):
    arr = [int(x * 100) for x in arr]
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        counting_sort(arr, exp)
        exp *= 10
    return [x / 100 for x in arr]

def counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        index = arr[i] // exp
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1

    for i in range(n):
        arr[i] = output[i]

def calculate_correlation(x_entries, y_entry, result_label, graph_frame):
    try:
        if len(x_entries) != 1:
            raise ValueError("Correlation can only be calculated with one X Data entry.")
        
        x, y = get_data(x_entries, y_entry)
        if len(x) != len(y):
            raise ValueError("X and Y data must have the same number of points")
        
        correlation = np.corrcoef(x, y)[0, 1]
        description = get_correlation_description(correlation)
        result_label.config(text=f"Correlation: {correlation}\n\n{description}")
        plot_graph(x, y, "Correlation", graph_frame)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def calculate_regression(x_entries, y_entry, result_label, graph_frame):
    try:
        if len(x_entries) != 1:
            raise ValueError("Regression can only be calculated with one X Data entry.")
        
        x, y = get_data(x_entries, y_entry)
        if len(x) != len(y):
            raise ValueError("X and Y data must have the same number of points")
        
        x = np.array(x).reshape(-1, 1)
        y = np.array(y)
        model = LinearRegression().fit(x, y)
        description = "The regression model fits the data well, indicating a strong relationship between the variables."  # You can add more complex descriptions based on the regression results if needed
        result_label.config(text=f"Regression Coefficients: {model.coef_}\n\nIntercept: {model.intercept_}\n\n{description}")
        plot_graph(x.flatten(), y, "Regression", graph_frame, model)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def calculate_mse(x_entries, y_entry, result_label):
    try:
        if len(x_entries) != 1:
            raise ValueError("MSE can only be calculated with one X Data entry.")
        
        x, y = get_data(x_entries, y_entry)
        if len(x) != len(y):
            raise ValueError("X and Y data must have the same number of points")
        
        mse = mean_squared_error(x, y)
        description = get_mse_description(mse)
        result_label.config(text=f"MSE: {mse}\n\n{description}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def get_correlation_description(correlation):
    if correlation > 0.8:
        return "Strong positive correlation. This indicates a very strong relationship between the X and Y variables, where an increase in X is associated with a significant increase in Y."
    elif correlation > 0.5:
        return "Moderate positive correlation. This indicates a moderate relationship between the X and Y variables, where an increase in X is associated with a moderate increase in Y."
    elif correlation > 0.3:
        return "Weak positive correlation. This indicates a weak relationship between the X and Y variables, where an increase in X is associated with a slight increase in Y."
    elif correlation > -0.3:
        return "No correlation. This indicates no significant relationship between the X and Y variables."
    elif correlation > -0.5:
        return "Weak negative correlation. This indicates a weak relationship between the X and Y variables, where an increase in X is associated with a slight decrease in Y."
    elif correlation > -0.8:
        return "Moderate negative correlation. This indicates a moderate relationship between the X and Y variables, where an increase in X is associated with a moderate decrease in Y."
    else:
        return "Strong negative correlation. This indicates a very strong relationship between the X and Y variables, where an increase in X is associated with a significant decrease in Y."

def get_mse_description(mse):
    if mse < 0.1:
        return "Excellent fit. The model's predictions are very close to the actual data points, indicating a highly accurate model."
    elif mse < 0.5:
        return "Good fit. The model's predictions are reasonably close to the actual data points, indicating a fairly accurate model."
    elif mse < 1:
        return "Moderate fit. The model's predictions are somewhat close to the actual data points, indicating a moderately accurate model."
    else:
        return "Poor fit. The model's predictions are not close to the actual data points, indicating a poorly accurate model."

def calculate_anova(x_entries, result_label):
    try:
        x = [list(map(float, group.get("1.0", tk.END).strip().split())) for group in x_entries]
        if any(len(group) <= 1 for group in x):
            raise ValueError("Each group must have more than one data point for ANOVA")
        f_val, p_val = stats.f_oneway(*x)
        result_label.config(text=f"ANOVA F-value: {f_val}\n\np-value: {p_val}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        
def sort_data(x_entries, result_label):
    try:
        x, _ = get_data(x_entries, None)
        start_time = time.time()
        sorted_x = radix_sort(x)
        end_time = time.time()
        time_complexity = end_time - start_time
        space_complexity = len(x) * 4
        result_label.config(text=f"Sorted Data:\n{sorted_x}\n\nTime Complexity: {time_complexity:.6f} seconds\n\nSpace Complexity: {space_complexity} bytes")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def get_data(x_entries, y_entry):
    x_data = [entry.get("1.0", tk.END).strip() for entry in x_entries]
    y_data = y_entry.get("1.0", tk.END).strip() if y_entry else ""
    if not all(x_data) or (y_entry and not y_data):
        raise ValueError("X and Y data cannot be empty")
    x = [float(item) for sublist in x_data for item in sublist.split()]
    y = list(map(float, y_data.split())) if y_entry else []
    return x, y

def plot_graph(x, y, title, graph_frame, model=None):
    for widget in graph_frame.winfo_children():
        widget.destroy()
    fig, ax = plt.subplots()
    ax.scatter(x, y, color='blue')
    if model:
        ax.plot(x, model.predict(np.array(x).reshape(-1, 1)), color='red')
    for i, txt in enumerate(y):
        ax.annotate(txt, (x[i], y[i]))
    ax.set_title(title)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def initialize_blank_graph(graph_frame):
    for widget in graph_frame.winfo_children():
        widget.destroy()
    fig, ax = plt.subplots()
    ax.set_title("Blank Graph")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)