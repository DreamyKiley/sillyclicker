import os
import pickle
import requests
from PIL import Image
import tempfile
import tkinter as tk
import webbrowser
from tkinter import messagebox
from shop_items import Upgrade, Autoclicker  # Import the classes for upgrades and autoclickers

def download_and_convert_icon(url, path):
    """Download an image from the given URL and convert it to .ico format."""
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, 'wb') as file:
            file.write(response.content)
        
        # Open the downloaded image
        with Image.open(path) as img:
            # Convert image to .ico format
            img.save(path, format='ICO')

class ClickerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Clicker Game")  # Window title
        self.root.geometry("600x400")  # Increased size for better view
        self.root.configure(bg="pink")  # Background color

        # Set window icon
        self.set_window_icon()

        # Initialize game state
        self.clicks = 0
        self.money = 0
        self.money_per_click = 1

        # Initialize the upgrade and autoclicker
        self.upgrade = Upgrade(cost=10, increment=1, max_level=10)
        self.autoclicker = Autoclicker(cost=5000)

        # Initialize GUI components
        self.init_gui()

        # Attempt to load saved game state
        if not self.load_game_state():
            self.reset_game_state()  # Reset game state if loading fails

        # Update labels to reflect the loaded or default game state
        self.update_labels()

        # Bind the close event to save game state
        self.root.protocol("WM_DELETE_WINDOW", self.save_and_exit)

    def set_window_icon(self):
        """Set the icon for the main game window."""
        icon_url = "https://avatars.githubusercontent.com/u/86751611?v=4"
        with tempfile.TemporaryDirectory() as temp_dir:
            icon_path = os.path.join(temp_dir, "github_icon.ico")
            download_and_convert_icon(icon_url, icon_path)
            self.root.iconbitmap(icon_path)

    def init_gui(self):
        """Initialize and set up the graphical user interface."""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a frame for the buttons and labels on the left side
        self.left_frame = tk.Frame(self.root, bg="pink")
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Create a label to show the number of clicks
        self.click_label = tk.Label(self.left_frame, text=f"Clicks: {self.clicks}", font=("Arial", 14), bg="pink", fg="purple")
        self.click_label.pack(pady=5)
        
        # Create a label to show the amount of money
        self.money_label = tk.Label(self.left_frame, text=f"Money: ${self.money}", font=("Arial", 14), bg="pink", fg="purple")
        self.money_label.pack(pady=5)
        
        # Create a damage label to display damage dealt
        self.damage_label = tk.Label(self.root, text="", font=("Arial", 12), bg="pink", fg="red")
        self.damage_label.pack()

        # Create an upgrade button
        self.upgrade_button = tk.Button(self.left_frame, text=self.upgrade.get_button_text(), font=("Arial", 12), bg="purple", fg="white", command=self.buy_upgrade)
        self.upgrade_button.pack(pady=10)
        
        # Create an autoclicker button
        self.autoclicker_button = tk.Button(self.left_frame, text=self.autoclicker.get_button_text(), font=("Arial", 12), bg="purple", fg="white", command=self.buy_autoclicker)
        self.autoclicker_button.pack(pady=10)

        # Create a credits button
        self.credits_button = tk.Button(self.left_frame, text="Credits", font=("Arial", 12), bg="purple", fg="white", command=self.open_credits)
        self.credits_button.pack(pady=10)

        # Create a canvas to draw the clickable box
        self.canvas = tk.Canvas(self.root, width=250, height=250, bg="purple", highlightthickness=0)
        self.canvas.pack(side=tk.RIGHT, padx=20, pady=10)
        self.draw_box()

        # Bind the click event to the canvas for incrementing clicks
        self.canvas.bind("<Button-1>", self.increment_click)

    def draw_box(self):
        """Draw a clickable box on the canvas."""
        self.canvas.create_rectangle(50, 50, 200, 200, outline="white", width=3)

    def increment_click(self, event=None):
        """Increment clicks and money on each canvas click."""
        self.clicks += 1
        self.money += self.money_per_click
        self.show_damage(self.money_per_click)  # Show damage text for fun
        self.update_labels()

    def show_damage(self, damage_amount):
        """Display the damage amount briefly before clearing it."""
        self.damage_label.config(text=f"Damage: ${damage_amount}")
        self.root.after(1000, lambda: self.damage_label.config(text=""))  # Clear text after 1 second

    def update_labels(self):
        """Update all labels and buttons to reflect current game state."""
        self.click_label.config(text=f"Clicks: {self.clicks}")
        self.money_label.config(text=f"Money: ${self.money}")
        
        # Update the upgrade button text and disable if max level reached
        self.upgrade_button.config(text=self.upgrade.get_button_text())
        if self.upgrade.level >= self.upgrade.max_level:
            self.upgrade_button.config(state=tk.DISABLED)

        # Update the autoclicker button text and disable if active
        self.autoclicker_button.config(text=self.autoclicker.get_button_text())
        if self.autoclicker.active:
            self.autoclicker_button.config(state=tk.DISABLED)

    def buy_upgrade(self):
        """Purchase an upgrade and adjust game state accordingly."""
        self.money, increment = self.upgrade.buy(self.money)
        self.money_per_click += increment
        self.update_labels()

    def buy_autoclicker(self):
        """Purchase an autoclicker and start it if activated."""
        self.money = self.autoclicker.buy(self.money)
        self.update_labels()
        if self.autoclicker.active:
            self.start_autoclicker()

    def start_autoclicker(self):
        """Start the autoclicker to click automatically at intervals."""
        if self.autoclicker.active:
            self.increment_click()
            self.root.after(1000, self.start_autoclicker)  # Auto-click every 1 second

    def open_credits(self):
        """Open a window to display credits and additional info."""
        credits_window = tk.Toplevel(self.root)
        credits_window.title("Credits")
        credits_window.geometry("350x200")
        credits_window.configure(bg="pink")

        # Set the icon for the credits window
        self.set_credits_icon(credits_window)

        # Credits Text
        text = tk.Text(credits_window, wrap=tk.WORD, height=6, width=40, font=("Arial", 12), bg="pink", bd=0, padx=10, pady=10)
        text.pack(pady=10)

        url = "https://allmylinks.com/dreamykiley"
        additional_text = "CLICK!"  # Customizable additional text

        text.insert(tk.END, "Clicker Game\n\nCredit: Kiley W.\nVisit: ")
        text.insert(tk.END, url, ('url',))
        text.tag_config('url', foreground='blue', underline=True)
        text.bind("<Button-1>", lambda e: webbrowser.open(url))

    def set_credits_icon(self, window):
        """Set the icon for the credits window."""
        icon_url = "https://avatars.githubusercontent.com/u/86751611?v=4"
        with tempfile.TemporaryDirectory() as temp_dir:
            icon_path = os.path.join(temp_dir, "github_icon.ico")
            download_and_convert_icon(icon_url, icon_path)
            window.iconbitmap(icon_path)

    def save_game_state(self):
        """Save the current game state to a file."""
        save_folder = "save"
        os.makedirs(save_folder, exist_ok=True)
        save_path = os.path.join(save_folder, "game_state.pkl")
        try:
            with open(save_path, 'wb') as file:
                pickle.dump({
                    'clicks': self.clicks,
                    'money': self.money,
                    'money_per_click': self.money_per_click,
                    'upgrade': self.upgrade.__dict__,
                    'autoclicker': self.autoclicker.__dict__,
                }, file)
            print(f"Game state saved successfully to {save_path}.")
        except Exception as e:
            print(f"Error saving game state: {e}")

    def load_game_state(self):
        """Load the saved game state from a file."""
        save_folder = "save"
        save_path = os.path.join(save_folder, "game_state.pkl")
        try:
            if os.path.exists(save_path):
                with open(save_path, 'rb') as file:
                    state = pickle.load(file)
                    self.clicks = state.get('clicks', 0)
                    self.money = state.get('money', 0)
                    self.money_per_click = state.get('money_per_click', 1)
                    self.upgrade.__dict__.update(state.get('upgrade', {}))
                    self.autoclicker.__dict__.update(state.get('autoclicker', {}))
                    print(f"Game state loaded successfully from {save_path}.")
                    return True
            else:
                print(f"No save file found at {save_path}.")
        except (pickle.PickleError, EOFError, IOError) as e:
            print(f"Failed to load save file: {e}. Resetting to default state.")
            self.reset_save_file()
        except Exception as e:
            print(f"Unexpected error while loading save file: {e}. Resetting to default state.")
            self.reset_save_file()
        return False

    def reset_save_file(self):
        """Remove corrupted save file and reset game state."""
        save_folder = "save"
        save_path = os.path.join(save_folder, "game_state.pkl")
        if os.path.exists(save_path):
            os.remove(save_path)
            print(f"Corrupted save file removed: {save_path}")
        
        # Reset game state
        self.reset_game_state()

        # Show reset message
        messagebox.showwarning("Save Corrupted", "Your save was corrupted, resetting to default state.")

    def reset_game_state(self):
        """Reset the game state to defaults and reinitialize GUI."""
        # Clear existing widgets and reinitialize the GUI
        self.init_gui()

        # Reset game state
        self.clicks = 0
        self.money = 0
        self.money_per_click = 1
        self.upgrade = Upgrade(cost=10, increment=1, max_level=10)
        self.autoclicker = Autoclicker(cost=5000)

        self.update_labels()

    def save_and_exit(self):
        """Save game state and exit the application."""
        self.save_game_state()
        self.root.destroy()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        game = ClickerGame(root)
        root.mainloop()
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        messagebox.showerror("Error", "An unexpected error occurred. Please check the console for details.")
