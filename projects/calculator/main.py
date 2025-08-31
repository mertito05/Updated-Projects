import tkinter as tk

def calculate():
    try:
        result = eval(entry.get())
        label_result.config(text="Result: " + str(result))
    except Exception as e:
        label_result.config(text="Error: " + str(e))

# Create the main window
root = tk.Tk()
root.title("Simple Calculator")

# Create an entry widget for user input
entry = tk.Entry(root, width=30)
entry.pack()

# Create a button to calculate the result
button_calculate = tk.Button(root, text="Calculate", command=calculate)
button_calculate.pack()

# Create a label to display the result
label_result = tk.Label(root, text="Result: ")
label_result.pack()

# Run the application
root.mainloop()
