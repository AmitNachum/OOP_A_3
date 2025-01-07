import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import pandas as pd

def load_csv():
    # Open a file dialog to select the CSV file
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    if not file_path:
        return  # No file selected

    try:
        # Read the CSV file using pandas
        df = pd.read_csv(file_path)

        # Clear the treeview
        for item in tree.get_children():
            tree.delete(item)
        tree["columns"] = list(df.columns)
        tree["show"] = "headings"

        # Set up the column headers
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Populate rows
        for _, row in df.iterrows():
            tree.insert("", tk.END, values=row.tolist())

        messagebox.showinfo("Success", "CSV file loaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Could not load file: {e}")

# Create the main window
root = tk.Tk()
root.title("CSV Viewer")

# Create a frame for the Treeview
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Add a Treeview widget
tree = ttk.Treeview(frame)
tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

# Add a scrollbar
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.configure(yscroll=scrollbar.set)

# Add a button to load CSV
btn_load = tk.Button(root, text="Load CSV", command=load_csv)
btn_load.pack(pady=10)

# Run the application
root.mainloop()
