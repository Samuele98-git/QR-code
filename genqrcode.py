import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import qrcode
from PIL import Image, ImageTk

# Define sizes as a list of (label, width, height) tuples
sizes = [
    ("100x100", 100, 100),
    ("200x200", 200, 200),
    ("300x300", 300, 300),
    ("400x400", 400, 400),
    ("500x500", 500, 500),
    ("600x600", 600, 600),
    ("700x700", 700, 700),
    ("800x800", 800, 800),
    ("900x900", 900, 900),
    ("1000x1000", 1000, 1000),
    ("1100x1100", 1100, 1100),
    ("1200x1200", 1200, 1200)
]

def generate_qr():
    # Get the URL or text from the entry widget
    url = url_entry.get().strip()  # Strip whitespace
    
    # Check if URL or text is empty
    if not url:
        messagebox.showerror("Error", "Please enter a URL or text.")
        return
    
    # Get the selected QR code size
    selected_size = size_var.get()
    width, height = [size[1:] for size in sizes if size[0] == selected_size][0]
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create an image from the QR Code instance
    qr_img = qr.make_image(fill_color="black", back_color="white").resize((width, height))
    
    # Convert PIL image to Tkinter PhotoImage
    global qr_img_tk
    qr_img_tk = ImageTk.PhotoImage(qr_img)
    
    # Display the QR code image
    qr_label.config(image=qr_img_tk)
    qr_label.image = qr_img_tk  # Keep a reference to prevent garbage collection
    
    # Save QR code image
    global saved_qr_img
    saved_qr_img = qr_img  # Keep a reference to the QR image for saving

def save_qr():
    try:
        # Ensure a QR code image has been generated and saved
        global saved_qr_img
        if saved_qr_img:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                                                     initialfile="qrcode.png")
            if file_path:
                # Save QR code image with custom name
                saved_qr_img.save(file_path)
                messagebox.showinfo("Success", "QR Code image saved successfully!")
        else:
            messagebox.showerror("Error", "Please generate a QR code first.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save QR Code image: {str(e)}")

# Create main window
root = tk.Tk()
root.title("QR Code Generator")

# Create URL entry
url_label = tk.Label(root, text="Enter URL or text:")
url_label.pack(pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.pack()

# Create dropdown for QR code size
size_label = tk.Label(root, text="Select QR Code Size:")
size_label.pack(pady=10)
size_var = tk.StringVar()
size_var.set(sizes[1][0])  # Default to Medium
size_dropdown = ttk.Combobox(root, textvariable=size_var, values=[size[0] for size in sizes])
size_dropdown.pack()

# Create generate button
generate_btn = tk.Button(root, text="Generate QR Code", command=generate_qr)
generate_btn.pack(pady=10)

# Create save button with custom name option
save_btn = tk.Button(root, text="Save QR Code", command=save_qr)
save_btn.pack(pady=10)

# Create label to display QR code image
qr_label = tk.Label(root)
qr_label.pack(pady=20)

# Initialize global variable to hold generated QR code image
saved_qr_img = None

# Run the GUI
root.mainloop()
