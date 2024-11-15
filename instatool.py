import tkinter as tk
from tkinter import filedialog, messagebox
import json

followers_data = None
following_data = None
followers = []
following = []

def open_file(file_type):
    global followers_data, following_data
    global followers
    global following

    file_path = filedialog.askopenfilename(
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                if file_type == "followers":
                    followers_data = data
                    for item in followers_data:
                        string_list_data = item.get('string_list_data')
                        followers.append(string_list_data[0].get('value'))
                    followers_label.config(text=f"Followers file loaded!")
                elif file_type == "following":
                    following_data = data.get('relationships_following')
                    for item in following_data:
                        string_list_data = item.get('string_list_data')
                        following.append(string_list_data[0].get('value'))
                    following_label.config(text=f"Following file loaded!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load JSON file: {e}")

def enter_action():
    if not followers_data or not following_data:
        messagebox.showerror("Error", "Both JSON files must be attached.")
        return
        
    desired_accounts = [account for account in following if account not in followers]

    new_window = tk.Toplevel(root)
    new_window.title("Accounts Not Following Back")

    result_label = tk.Label(new_window, text=f"Accounts Not Following Back: {len(desired_accounts)}")
    result_label.pack(pady=10)

    result_text = tk.Text(new_window, wrap=tk.WORD, height=20, width=50)
    result_text.pack(pady=10)
    for account in desired_accounts:
        result_text.insert(tk.END, f"{account}\n")

# Create the main application window
root = tk.Tk()
root.title("JSON File Loader")

# Create and place the button to open the file dialog for followers
followers_button = tk.Button(root, text="Attach Followers JSON File", command=lambda: open_file("followers"))
followers_button.pack(pady=10)

# Label to display the selected followers file path
followers_label = tk.Label(root, text="No followers file attached")
followers_label.pack(pady=10)

# Create and place the button to open the file dialog for following
following_button = tk.Button(root, text="Attach Following JSON File", command=lambda: open_file("following"))
following_button.pack(pady=10)

# Label to display the selected following file path
following_label = tk.Label(root, text="No following file attached")
following_label.pack(pady=10)

# Create and place the Enter button
enter_button = tk.Button(root, text="Enter", command=enter_action)
enter_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()