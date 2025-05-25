

def clear_screen(widget):  # destroys all child widgets under the given widget/frame
    for widget in widget.winfo_children():
        widget.destroy()