from datetime import datetime


def clear_screen(widget):  # destroys all child widgets under the given widget/frame
    for widget in widget.winfo_children():
        widget.destroy()


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")