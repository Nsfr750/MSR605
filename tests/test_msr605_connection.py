#!/usr/bin/env python3
"""
Test script that mimics the exact MSR605 connection process
with a GUI for results display
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from script.cardReader import CardReader
from script import cardReaderExceptions

class MSR605TestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MSR605 Connection Test")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Center the window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="MSR605 Connection Test", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Port selection
        port_label = ttk.Label(main_frame, text="COM Port:", font=('Arial', 10))
        port_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.port_var = tk.StringVar(value="COM2")
        self.port_combo = ttk.Combobox(main_frame, textvariable=self.port_var, 
                                       values=["COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8"],
                                       width=15)
        self.port_combo.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Test button
        self.test_button = ttk.Button(main_frame, text="Test Connection", 
                                     command=self.start_test, style="Accent.TButton")
        self.test_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Output text area
        output_label = ttk.Label(main_frame, text="Test Results:", font=('Arial', 10, 'bold'))
        output_label.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        self.output_text = scrolledtext.ScrolledText(main_frame, height=15, width=70, 
                                                     wrap=tk.WORD, font=('Courier', 9))
        self.output_text.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Configure grid weights for output area
        main_frame.rowconfigure(5, weight=1)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Configure style
        style = ttk.Style()
        style.configure("Accent.TButton", font=('Arial', 10, 'bold'))
        
    def log_message(self, message):
        """Add a message to the output text area"""
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.root.update_idletasks()
        
    def start_test(self):
        """Start the connection test in a separate thread"""
        self.test_button.config(state='disabled')
        self.port_combo.config(state='disabled')
        self.progress.start()
        self.status_var.set("Testing connection...")
        self.output_text.delete(1.0, tk.END)
        
        # Start test in separate thread to prevent GUI freezing
        test_thread = threading.Thread(target=self.run_test)
        test_thread.daemon = True
        test_thread.start()
        
    def run_test(self):
        """Run the actual connection test"""
        port = self.port_var.get()
        
        try:
            self.log_message(f"Testing MSR605 connection to {port}...")
            self.log_message(f"Creating CardReader instance...")
            
            # This mimics the UI code exactly
            msr = CardReader(port)
            self.log_message(f"✓ CardReader instance created")
            
            self.log_message(f"Attempting to connect...")
            msr.connect()
            self.log_message(f"✓ Successfully connected to {port}")
            
            # Test basic communication
            self.log_message(f"Testing communication...")
            msr.communication_test()
            self.log_message(f"✓ Communication test passed")
            
            # Clean up
            self.log_message(f"Closing connection...")
            msr.close_serial_connection()
            self.log_message(f"✓ Connection closed")
            
            success = True
            
        except cardReaderExceptions.MSR605ConnectError as e:
            self.log_message(f"✗ MSR605 Connection Error: {e}")
            success = False
        except PermissionError as e:
            self.log_message(f"✗ Permission Error: {e}")
            self.log_message(f"  This usually means you need to run as Administrator")
            success = False
        except Exception as e:
            self.log_message(f"✗ Unexpected Error: {e}")
            self.log_message(f"  Error type: {type(e).__name__}")
            success = False
        
        # Update GUI from main thread
        self.root.after(0, self.test_completed, success)
        
    def test_completed(self, success):
        """Handle test completion"""
        self.progress.stop()
        self.test_button.config(state='normal')
        self.port_combo.config(state='readonly')
        
        if success:
            self.status_var.set("✓ SUCCESS: Connection test passed!")
            self.log_message(f"\n" + "="*50)
            self.log_message(f"✓ SUCCESS: MSR605 connection works perfectly!")
            self.log_message(f"  Your application should be able to connect to {self.port_var.get()}")
            messagebox.showinfo("Success", "MSR605 connection test passed!\nYour device is working correctly.")
        else:
            self.status_var.set("✗ FAILED: Connection test failed")
            self.log_message(f"\n" + "="*50)
            self.log_message(f"✗ FAILED: Could not connect to {self.port_var.get()}")
            self.log_message(f"\nSOLUTIONS:")
            self.log_message(f"1. Run this application as Administrator:")
            self.log_message(f"   Right-click → 'Run as administrator'")
            self.log_message(f"2. Close any other applications that might be using {self.port_var.get()}")
            self.log_message(f"3. Check Windows Device Manager for port conflicts")
            self.log_message(f"4. Try unplugging and replugging the MSR605 device")
            self.log_message(f"5. Update Prolific USB-to-Serial drivers")
            
            messagebox.showerror("Failed", 
                              f"Could not connect to {self.port_var.get()}\n\n"
                              f"Check the test results for solutions.")

def main():
    """Main function to run the test application"""
    root = tk.Tk()
    app = MSR605TestApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()