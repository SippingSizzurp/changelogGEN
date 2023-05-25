import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import datetime
import importlib
import subprocess

# List of required packages
required_packages = ['tkinter', 'requests']

# Check if each required package is installed
missing_packages = []
for package in required_packages:
    try:
        importlib.import_module(package)
    except ImportError:
        missing_packages.append(package)

# Install missing packages using pip
if missing_packages:
    print("Installing missing packages...")
    for package in missing_packages:
        subprocess.check_call(['pip', 'install', package])
    print("Missing packages installed successfully.")
    
import requests

change_log_entries = []  # List to store change log entries
webhook_file = "webhook.txt"  # File to store the Discord webhook URL


def create_change_log():
    added_text = added_entry.get("1.0", tk.END).strip()
    removed_text = removed_entry.get("1.0", tk.END).strip()
    changed_text = changed_entry.get("1.0", tk.END).strip()
    fixed_text = fixed_entry.get("1.0", tk.END).strip()

    change_log_entries.clear()  # Clear the existing change log entries

    # Add the header with the current date
    change_log_entries.append(f"# CHANGE LOG {datetime.date.today()}\n")

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
    change_log_text.delete("1.0", tk.END)
    change_log_text.insert(tk.END, '\n'.join(change_log_entries))


def copy_to_clipboard():
    change_log = change_log_text.get("1.0", tk.END)
    root.clipboard_clear()
    root.clipboard_append(change_log)
    messagebox.showinfo("Copy to Clipboard", "Change Log copied to clipboard.")

def post_to_discord_webhook():
    webhook_url = webhook_entry.get().strip()
    change_log = change_log_text.get("1.0", tk.END)

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


root = tk.Tk()
root.title("Change Log")
root.configure(bg='#333333')  # Set the background color

# Configure column and row weights for resizing
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(7, weight=1)

# Define dark mode color scheme
style = ttk.Style()
style.theme_use('clam')
style.configure('TLabel', background='#333333', foreground='white')
style.configure('TEntry', fieldbackground='#1f1f1f', foreground='white')
style.configure('TButton', background='#1f1f1f', foreground='white')
style.configure('TText', background='#1f1f1f', foreground='white')

# Create the entry boxes
added_label = ttk.Label(root, text="ADDED")
added_label.grid(row=0, column=0, pady=5, padx=10, sticky="w")
added_entry = tk.Text(root, width=30, height=2, bg='#1f1f1f', fg='white')
added_entry.grid(row=1, column=0, padx=10, ipady=40, sticky="we")

removed_label = ttk.Label(root, text="REMOVED")
removed_label.grid(row=2, column=0, pady=5, padx=10, sticky="w")
removed_entry = tk.Text(root, width=30, height=2, bg='#1f1f1f', fg='white')
removed_entry.grid(row=3, column=0, padx=10, ipady=40, sticky="we")

changed_label = ttk.Label(root, text="CHANGED")
changed_label.grid(row=4, column=0, pady=5, padx=10, sticky="w")
changed_entry = tk.Text(root, width=30, height=2, bg='#1f1f1f', fg='white')
changed_entry.grid(row=5, column=0, padx=10, ipady=40, sticky="we")

fixed_label = ttk.Label(root, text="FIXED")
fixed_label.grid(row=6, column=0, pady=5, padx=10, sticky="w")
fixed_entry = tk.Text(root, width=30, height=2, bg='#1f1f1f', fg='white')
fixed_entry.grid(row=7, column=0, padx=10, ipady=40, sticky="we")

# Create the change log text widget
change_log_text = tk.Text(root, width=40, height=20, bg='#1f1f1f', fg='white')
change_log_text.grid(row=0, column=1, rowspan=8, padx=10, pady=10, ipady=100, sticky="nsew")


# Create the Discord webhook URL entry
webhook_label = ttk.Label(root, text="Discord Webhook URL")
webhook_label.grid(row=8, column=0, pady=5, padx=10, sticky="w")
webhook_entry = ttk.Entry(root, width=30)
webhook_entry.grid(row=8, column=1, padx=10, ipadx=100, sticky="we")

# Load the webhook URL and populate the entry if available
webhook_url = load_webhook_url()
webhook_entry.insert(tk.END, webhook_url)

# Create the button to update the change log
update_button = ttk.Button(root, text="Update Change Log", command=create_change_log)
update_button.grid(row=9, column=0, columnspan=2, pady=(10, 0), sticky="nsew")

# Create the button to copy the change log to clipboard
copy_button = ttk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.grid(row=10, column=0, columnspan=2, pady=(5, 0), sticky="nsew")

# Create the button to post the change log to Discord
post_button = ttk.Button(root, text="Post to Discord", command=post_to_discord_webhook)
post_button.grid(row=11, column=0, columnspan=2, pady=(5, 10), sticky="nsew")

root.mainloop()
