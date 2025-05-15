import tkinter as tk
import webbrowser

# Sponsor Class
class Sponsor:
    def __init__(self, root):
        self.root = root

    def show_sponsor(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Sponsor the Project")
        dialog.geometry('500x150')
        
        # Sponsor buttons
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=20)
        
        buttons = [
            ("Sponsor on GitHub", "https://github.com/sponsors/Nsfr750"),
            ("Join Discord", "https://discord.gg/BvvkUEP9"),
            ("Buy Me a Coffee", "https://paypal.me/3dmega"),
            ("Join The Patreon", "https://www.patreon.com/Nsfr750")
        ]
        
        for text, url in buttons:
            btn = tk.Button(btn_frame, text=text, pady=5,
                          command=lambda u=url: webbrowser.open(u))
            btn.pack(side=tk.LEFT, padx=5)
        
        # Close button
        tk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)

