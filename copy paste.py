import tkinter as tk
from tkinter import messagebox

def remove_line_spaces():
    input_text = input_text_widget.get("1.0", "end-1c")  # Get input text
    # Remove empty lines and join text into a single line
    lines = input_text.splitlines()
    non_empty_lines = [line.strip() for line in lines if line.strip() != '']
    output_text = ' '.join(non_empty_lines)
    output_text_widget.delete("1.0", "end")  # Clear previous output
    output_text_widget.insert("1.0", output_text)  # Insert new output

def copy_output():
    # Copy the output text to clipboard
    output_text = output_text_widget.get("1.0", "end-1c")
    root.clipboard_clear()
    root.clipboard_append(output_text)
    messagebox.showinfo("Copied", "Output text has been copied to clipboard!")

def paste_input():
    # Paste text from clipboard into the input text box
    input_text = root.clipboard_get()
    input_text_widget.delete("1.0", "end")
    input_text_widget.insert("1.0", input_text)

# Create the main window
root = tk.Tk()
root.title("Text Processor")

# Create input text box
input_text_widget = tk.Text(root, height=10, width=50)
input_text_widget.pack(pady=10)

# Create buttons for pasting, processing and copying
paste_button = tk.Button(root, text="Paste", command=paste_input)
paste_button.pack(side=tk.LEFT, padx=10)

process_button = tk.Button(root, text="Process", command=remove_line_spaces)
process_button.pack(side=tk.LEFT, padx=10)

# Create output text box
output_text_widget = tk.Text(root, height=10, width=50)
output_text_widget.pack(pady=10)

# Create copy button for output text
copy_button = tk.Button(root, text="Copy", command=copy_output)
copy_button.pack(pady=10)

# Run the application
root.mainloop()
