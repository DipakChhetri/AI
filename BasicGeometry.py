from owlready2 import *
import tkinter as tk
from tkinter import ttk, messagebox
import math

# Load the ontology
ontology_path = "BasicGeometryOntology.owl"
ontology = get_ontology(r"C:\Users\Swift\Desktop\AI\BasicGeometryOntology.owl").load()

# Function to fetch classes
def fetch_classes():
    return [cls.name for cls in ontology.classes()]

# Function to fetch individuals of a class
def fetch_individuals(class_name):
    cls = ontology.search_one(iri=f"*{class_name}")
    if cls:
        return [ind.name for ind in cls.instances()]
    else:
        return []

# Function to fetch properties of an individual
def fetch_properties(individual_name):
    individual = ontology.search_one(iri=f"*{individual_name}")
    if individual:
        object_props = {}
        for prop in ontology.object_properties():
            values = prop[individual]
            if values:
                object_props[prop.name] = [val.name for val in values]
        data_props = {}
        for prop in ontology.data_properties():
            values = prop[individual]
            if values:
                data_props[prop.name] = values
        return object_props, data_props
    else:
        return {}, {}

# Function to calculate area and perimeter for different shapes
def calculate_area_and_perimeter(shape, dimension1, dimension2=None):
    if shape == "Circle":
        area = math.pi * (dimension1 ** 2)  # radius squared
        perimeter = 2 * math.pi * dimension1  # circumference
    elif shape == "Square":
        area = dimension1 ** 2  # side squared
        perimeter = 4 * dimension1  # 4 sides
    elif shape == "EquilateralTriangle":
        area = (math.sqrt(3) / 4) * (dimension1 ** 2)  # area formula for equilateral triangle
        perimeter = 3 * dimension1  # 3 equal sides
    elif shape == "IsoscelesTriangle":
        # Assuming isosceles triangle with given base and height
        area = 0.5 * dimension1 * dimension2  # base * height / 2
        perimeter = dimension1 + 2 * math.sqrt((dimension2 ** 2) + (dimension1 / 2) ** 2)  # Perimeter calculation
    else:
        area = perimeter = 0
    return area, perimeter

# GUI Functions
def show_classes():
    class_list.delete(0, tk.END)
    for cls in fetch_classes():
        class_list.insert(tk.END, cls)

def on_class_select(event):
    selected_class = class_list.get(class_list.curselection())
    individuals = fetch_individuals(selected_class)
    individual_list.delete(0, tk.END)
    for ind in individuals:
        individual_list.insert(tk.END, ind)

def on_individual_select(event):
    selected_individual = individual_list.get(individual_list.curselection())
    object_props, data_props = fetch_properties(selected_individual)

    # Display Object Properties
    object_prop_list.delete(*object_prop_list.get_children())
    for prop, values in object_props.items():
        object_prop_list.insert("", tk.END, values=(prop, ", ".join(values)))

    # Display Data Properties
    data_prop_list.delete(*data_prop_list.get_children())
    for prop, values in data_props.items():
        data_prop_list.insert("", tk.END, values=(prop, ", ".join(values)))

def perform_calculation():
    shape = shape_entry.get().strip()
    dimension1 = float(dimension1_entry.get().strip())

    # Assuming a second dimension for certain shapes like Isosceles Triangle
    if shape == "IsoscelesTriangle":
        dimension2 = float(dimension2_entry.get().strip())
    else:
        dimension2 = None  # Not needed for other shapes

    # Calculate area and perimeter
    area, perimeter = calculate_area_and_perimeter(shape, dimension1, dimension2)

    # Show the results
    result_label.config(text=f"Area: {area:.2f} sq. units, Perimeter: {perimeter:.2f} units")

# Create GUI
root = tk.Tk()
root.title("Ontology Viewer - Basic Geometry ")
root.geometry("700x600")  # Set window size
root.config(bg="#f0f0f0")  # Set background color

# Frames
frame1 = tk.Frame(root, bg="#f0f0f0")
frame1.pack(side=tk.LEFT, padx=20, pady=20)

frame2 = tk.Frame(root, bg="#f0f0f0")
frame2.pack(side=tk.LEFT, padx=20, pady=20)

frame3 = tk.Frame(root, bg="#f0f0f0")
frame3.pack(side=tk.LEFT, padx=20, pady=20)

# Class List
tk.Label(frame1, text="Select Geometry Classes", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)
class_list = tk.Listbox(frame1, height=15, width=30, font=("Arial", 12), bg="#ffffff", selectmode=tk.SINGLE)
class_list.pack()
class_list.bind("<<ListboxSelect>>", on_class_select)
tk.Button(frame1, text="Load Classes", command=show_classes, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=10)

# Individual List
tk.Label(frame2, text="Select Individuals", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)
individual_list = tk.Listbox(frame2, height=15, width=30, font=("Arial", 12), bg="#ffffff", selectmode=tk.SINGLE)
individual_list.pack()
individual_list.bind("<<ListboxSelect>>", on_individual_select)

# Object Properties Table
tk.Label(frame3, text="Object Properties", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)
object_prop_list = ttk.Treeview(frame3, columns=("Property", "Value"), show="headings", height=8)
object_prop_list.heading("Property", text="Property", anchor=tk.W)
object_prop_list.heading("Value", text="Value", anchor=tk.W)
object_prop_list.pack(padx=10, pady=10)

# Data Properties Table
tk.Label(frame3, text="Data Properties", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)
data_prop_list = ttk.Treeview(frame3, columns=("Property", "Value"), show="headings", height=8)
data_prop_list.heading("Property", text="Property", anchor=tk.W)
data_prop_list.heading("Value", text="Value", anchor=tk.W)
data_prop_list.pack(padx=10, pady=10)

# Shape Calculation Frame
calc_frame = tk.Frame(root, bg="#f0f0f0")
calc_frame.pack(side=tk.BOTTOM, padx=20, pady=20)

# Heading for Calculation
tk.Label(calc_frame, text="Geometry Shape Calculator", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

# Shape Input
tk.Label(calc_frame, text="Shape (Circle, Square, EquilateralTriangle, IsoscelesTriangle)", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
shape_entry = tk.Entry(calc_frame, font=("Arial", 12), bg="#ffffff", width=20)
shape_entry.pack(pady=5)

# Dimension Inputs
tk.Label(calc_frame, text="Dimension 1 (Radius for Circle, Side for Square/Triangle)", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
dimension1_entry = tk.Entry(calc_frame, font=("Arial", 12), bg="#ffffff", width=20)
dimension1_entry.pack(pady=5)

# Second dimension for shapes that need it (like Isosceles Triangle)
tk.Label(calc_frame, text="Dimension 2 (Height for Triangle, leave blank if not needed)", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
dimension2_entry = tk.Entry(calc_frame, font=("Arial", 12), bg="#ffffff", width=20)
dimension2_entry.pack(pady=5)

# Calculate Button
tk.Button(calc_frame, text="Calculate Area and Perimeter", command=perform_calculation, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=10)

# Result Display
result_label = tk.Label(calc_frame, text="Area: , Perimeter: ", font=("Arial", 12, "bold"), bg="#f0f0f0")
result_label.pack()

# Run the Application
root.mainloop()
