import tkinter as tk
from tkinter import ttk, messagebox

# Default power ratings for common appliances
DEFAULT_POWER_RATINGS = {
    "Fan": 70,
    "Fridge": 150,
    "Washing Machine": 500,
    "TV": 100,
    "Air Conditioner": 1500,
    "Heater": 2000,
    "Laptop": 50,
    "Light Bulb": 10,
}

# List to store appliances
appliances = []

# Function to add appliances
def add_appliance():
    appliance_name = appliance_var.get()
    hours_used = hours_var.get()

    if not appliance_name or not hours_used:
        messagebox.showerror("Input Error", "Please enter the appliance name and usage time.")
        return

    power = power_var.get()
    if not power:
        power = DEFAULT_POWER_RATINGS.get(appliance_name)
        if power is None:
            messagebox.showerror("Input Error", "Please enter a power rating for this appliance.")
            return
    else:
        try:
            power = float(power)
        except ValueError:
            messagebox.showerror("Input Error", "Power rating must be a valid number.")
            return

    try:
        hours_used = float(hours_used)
    except ValueError:
        messagebox.showerror("Input Error", "Usage time must be a valid number.")
        return

    appliances.append({"name": appliance_name, "power": power, "hours": hours_used})
    appliance_listbox.insert(tk.END, f"{appliance_name} - {power} W, {hours_used} hours")
    appliance_var.set("")
    power_var.set("")
    hours_var.set("")

# Function to remove selected appliance
def remove_selected_appliance():
    selected_index = appliance_listbox.curselection()
    if selected_index:
        appliance_listbox.delete(selected_index)
        del appliances[selected_index[0]]
    else:
        messagebox.showerror("Selection Error", "Please select an appliance to remove.")

# Function to calculate savings
def calculate_savings():
    grid_cost = grid_cost_var.get()
    renewable_cost = renewable_cost_var.get()

    if not grid_cost or not renewable_cost:
        messagebox.showerror("Input Error", "Please enter the grid and renewable energy costs.")
        return

    try:
        grid_cost = float(grid_cost)
        renewable_cost = float(renewable_cost)
    except ValueError:
        messagebox.showerror("Input Error", "Costs must be valid numbers.")
        return

    total_consumption = 0
    total_grid_cost = 0
    total_renewable_cost = 0

    # Calculate total energy consumption and cost
    for appliance in appliances:
        power_kw = appliance["power"] / 1000  # Convert watts to kilowatts
        consumption_kwh = power_kw * appliance["hours"]  # Consumption in kWh
        total_consumption += consumption_kwh
        total_grid_cost += consumption_kwh * grid_cost
        total_renewable_cost += consumption_kwh * renewable_cost

    total_savings = total_grid_cost - total_renewable_cost

    result_text = (
        "Energy Savings Calculation:\n\n"
        f"Total Appliances: {len(appliances)}\n"
        f"Total Power Consumption: {total_consumption:.2f} kWh\n"
        f"Total Cost with Grid Electricity: ${total_grid_cost:.2f}\n"
        f"Total Cost with Renewable Energy: ${total_renewable_cost:.2f}\n"
        f"Total Energy Savings: ${total_savings:.2f}\n\n"
        "Breakdown by Appliance:\n"
    )

    for idx, appliance in enumerate(appliances, start=1):
        result_text += (
            f"{idx}. {appliance['name']} - {appliance['power']} W, "
            f"{appliance['hours']} hours, "
            f"{appliance['power'] * appliance['hours'] / 1000:.2f} kWh\n"
        )

    # Display results in the text box
    result_text_widget.config(state="normal")
    result_text_widget.delete("1.0", tk.END)
    result_text_widget.insert(tk.END, result_text)
    result_text_widget.config(state="disabled")

    # Save results to a file
    with open("energy_savings_results.txt", "a") as file:
        file.write(result_text + "\n")

# Function to clear the results
def clear_results():
    result_text_widget.config(state="normal")
    result_text_widget.delete("1.0", tk.END)
    result_text_widget.config(state="disabled")

# Create main window
root = tk.Tk()
root.title("Energy Savings Calculator")
root.geometry("600x700")
root.resizable(False, False)

# Title
title_label = ttk.Label(root, text="Appliance Energy Savings Calculator", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Appliance input frame
appliance_frame = ttk.LabelFrame(root, text="Add Appliance")
appliance_frame.pack(padx=10, pady=5, fill="x")

# Appliance dropdown
appliance_label = ttk.Label(appliance_frame, text="Select Appliance:")
appliance_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
appliance_var = tk.StringVar()
appliance_entry = ttk.Combobox(appliance_frame, textvariable=appliance_var, values=list(DEFAULT_POWER_RATINGS.keys()))
appliance_entry.grid(row=0, column=1, padx=5, pady=5)

# Power input field
power_label = ttk.Label(appliance_frame, text="Power (W):")
power_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
power_var = tk.StringVar()
power_entry = ttk.Entry(appliance_frame, textvariable=power_var)
power_entry.grid(row=1, column=1, padx=5, pady=5)

# Hours input field
hours_label = ttk.Label(appliance_frame, text="Usage (Hours):")
hours_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
hours_var = tk.StringVar()
hours_entry = ttk.Entry(appliance_frame, textvariable=hours_var)
hours_entry.grid(row=2, column=1, padx=5, pady=5)

# Add Appliance Button
add_button = ttk.Button(appliance_frame, text="Add Appliance", command=add_appliance)
add_button.grid(row=3, column=0, columnspan=2, pady=10)

# Appliance list frame
list_frame = ttk.LabelFrame(root, text="Appliance List")
list_frame.pack(padx=10, pady=5, fill="x")

appliance_listbox = tk.Listbox(list_frame, height=10, width=50)
appliance_listbox.pack(pady=5)

remove_button = ttk.Button(list_frame, text="Remove Selected", command=remove_selected_appliance)
remove_button.pack(pady=5)

# Cost input frame
cost_frame = ttk.LabelFrame(root, text="Electricity Costs")
cost_frame.pack(padx=10, pady=5, fill="x")

# Grid cost input field
grid_cost_label = ttk.Label(cost_frame, text="Grid Electricity Cost (per kWh):")
grid_cost_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
grid_cost_var = tk.StringVar()
grid_cost_entry = ttk.Entry(cost_frame, textvariable=grid_cost_var)
grid_cost_entry.grid(row=0, column=1, padx=5, pady=5)

# Renewable energy cost input field
renewable_cost_label = ttk.Label(cost_frame, text="Renewable Energy Cost (per kWh):")
renewable_cost_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
renewable_cost_var = tk.StringVar()
renewable_cost_entry = ttk.Entry(cost_frame, textvariable=renewable_cost_var)
renewable_cost_entry.grid(row=1, column=1, padx=5, pady=5)

# Calculate and Clear Buttons
calculate_button = ttk.Button(cost_frame, text="Calculate Savings", command=calculate_savings)
calculate_button.grid(row=2, column=0, pady=10, padx=5)

clear_button = ttk.Button(cost_frame, text="Clear Results", command=clear_results)
clear_button.grid(row=2, column=1, pady=10, padx=5)

# Results frame
result_frame = ttk.LabelFrame(root, text="Results")
result_frame.pack(padx=10, pady=5, fill="both", expand=True)

result_text_widget = tk.Text(result_frame, height=10, width=70, state="disabled", wrap="word", font=("Arial", 10))
result_text_widget.pack(pady=5, padx=5)

# Scrollbar for the results
scrollbar = ttk.Scrollbar(result_frame, command=result_text_widget.yview)
result_text_widget.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Run the application
root.mainloop()
