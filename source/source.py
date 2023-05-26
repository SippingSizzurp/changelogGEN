from pathlib import Path
import datetime
import tkinter.messagebox as messagebox
from tkinter import *
import tkinter as tk
import requests


ASSETS_PATH = Path(r"./assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


webhook_file = "webhook.txt"  # File to store the Discord webhook URL


def create_change_log():
    added_text = entry_2.get("1.0", tk.END).strip()
    removed_text = entry_3.get("1.0", tk.END).strip()
    changed_text = entry_4.get("1.0", tk.END).strip()
    fixed_text = entry_5.get("1.0", tk.END).strip()

    change_log_entries = [f"# CHANGE LOG {datetime.date.today()}\n"]  # Create an empty list to store the change log entries

    # Add the header with the current date

    if added_text:
        change_log_entries.append("- ### __ADDED__")
        change_log_entries.extend([f' - {line}' for line in added_text.split('\n') if line])
        change_log_entries.append('')
    if removed_text:
        change_log_entries.append("- ### __REMOVED__")
        change_log_entries.extend([f' - {line}' for line in removed_text.split('\n') if line])
        change_log_entries.append('')
    if changed_text:
        change_log_entries.append("- ### __CHANGED__")
        change_log_entries.extend([f' - {line}' for line in changed_text.split('\n') if line])
        change_log_entries.append('')
    if fixed_text:
        change_log_entries.append("- ### __FIXED__")
        change_log_entries.extend([f' - {line}' for line in fixed_text.split('\n') if line])
        change_log_entries.append('')

    # Display the entire change log in the text widget
    entry_1.delete("1.0", tk.END)
    entry_1.insert(tk.END, '\n'.join(change_log_entries))


def copy_to_clipboard():
    change_log = entry_1.get("1.0", tk.END)
    window.clipboard_clear()
    window.clipboard_append(change_log)
    messagebox.showinfo("Copy to Clipboard", "Change Log copied to clipboard.")


def post_to_discord_webhook():
    webhook_url = entry_6.get().strip()
    change_log = entry_1.get("1.0", tk.END)

    if not webhook_url:
        messagebox.showwarning("Missing Webhook URL", "Please enter a valid Discord webhook URL.")
        return

    # Perform the POST request to the Discord webhook URL
    try:
        response = requests.post(webhook_url, json={"content": change_log})
        response.raise_for_status()
        messagebox.showinfo("Webhook Post Success", "Change Log posted to Discord successfully.")

        # Save the updated webhook URL
        save_webhook_url(webhook_url)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Webhook Post Error", f"An error occurred while posting to Discord:\n{e}")


def save_webhook_url(url):
    with open(webhook_file, "w") as file:
        file.write(url)


def load_webhook_url():
    try:
        with open(webhook_file, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""


window = Tk()

window.geometry("800x631")
window.configure(bg="#292B2F")
window.title("Change-Log Generator")


canvas = Canvas(
    window,
    bg="#292B2F",
    height=631,
    width=800,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_rectangle(
    0.0,
    0.0,
    231.0,
    631.0,
    fill="#2F3136",
    outline="")

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    519.5,
    216.5,
    image=entry_image_1
)
entry_1 = Text(
    bd=0,
    bg="#40444B",
    fg="white",
    highlightthickness=0
)
entry_1.place(
    x=269.0,
    y=32.0,
    width=501.0,
    height=367.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    115.0,
    88.0,
    image=entry_image_2
)
entry_2 = Text(
    bd=0,
    bg="#40444B",
    fg="white",
    highlightthickness=0
)
entry_2.place(
    x=19.0,
    y=32.0,
    width=192.0,
    height=110.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    115.0,
    556.0,
    image=entry_image_3
)
entry_3 = Text(
    bd=0,
    bg="#40444B",
    fg="white",
    highlightthickness=0
)
entry_3.place(
    x=19.0,
    y=500.0,
    width=192.0,
    height=110.0
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    115.0,
    244.0,
    image=entry_image_4
)
entry_4 = Text(
    bd=0,
    bg="#40444B",
    fg="white",
    highlightthickness=0
)
entry_4.place(
    x=19.0,
    y=188.0,
    width=192.0,
    height=110.0
)

entry_image_5 = PhotoImage(
    file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(
    115.0,
    400.0,
    image=entry_image_5
)
entry_5 = Text(
    bd=0,
    bg="#40444B",
    fg="white",
    highlightthickness=0
)
entry_5.place(
    x=19.0,
    y=344.0,
    width=192.0,
    height=110.0,
)

canvas.create_text(
    12.0,
    12.0,
    anchor="nw",
    text="ADDED",
    fill="#FFFFFF",
    font=("Inter", 15 * -1)
)

canvas.create_text(
    12.0,
    168.0,
    anchor="nw",
    text="REMOVED",
    fill="#FFFFFF",
    font=("Inter", 15 * -1)
)

canvas.create_text(
    12.0,
    324.0,
    anchor="nw",
    text="CHANGED",
    fill="#FFFFFF",
    font=("Inter", 15 * -1)
)

canvas.create_text(
    12.0,
    480.0,
    anchor="nw",
    text="FIXED",
    fill="#FFFFFF",
    font=("Inter", 15 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=create_change_log,
    relief="flat"
)
button_1.place(
    x=282.0,
    y=410.0,
    width=118.0,
    height=29.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=copy_to_clipboard,
    relief="flat"
)
button_2.place(
    x=460.0,
    y=410.0,
    width=118.0,
    height=29.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=post_to_discord_webhook,
    relief="flat"
)
button_3.place(
    x=638.0,
    y=410.0,
    width=118.0,
    height=29.0
)

entry_image_6 = PhotoImage(
    file=relative_to_assets("entry_6.png"))
entry_bg_6 = canvas.create_image(
    519.0,
    516.5,
    image=entry_image_6
)
entry_6 = Entry(
    bd=0,
    bg="#40444B",
    fg="white",
    highlightthickness=0
)
entry_6.place(
    x=282.0,
    y=499.0,
    width=474.0,
    height=33.0
)

canvas.create_text(
    282.0,
    480.0,
    anchor="nw",
    text="Discord Webhook URL",
    fill="#FFFFFF",
    font=("Inter", 15 * -1)
)
window.resizable(False, False)
webhook_url = load_webhook_url()
entry_6.insert(tk.END, webhook_url)
window.mainloop()
