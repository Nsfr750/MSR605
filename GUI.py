#!/usr/bin/env python3

import tkinter as tk
import sys, time, cardReaderExceptions, io
from cardReader import CardReader
from tkinter import *
from tkinter import ttk, messagebox, filedialog, font
from tkinter.messagebox import *
import serial, serial.tools.list_ports
import os, sqlite3, csv
from datetime import datetime
from advanced_functions import AdvancedFunctionsFrame
from updates import check_for_updates

class GUI(Frame):    
    def __init__(self, parent):
        Frame.__init__(self, parent)


        
        self.__coercivityRadioBtnValue = StringVar()
        self.__coercivityRadioBtnValue.set('hi')
        
        self.__autoSaveDatabase = BooleanVar()
        self.__autoSaveDatabase.set(False)
        
        self.__enableDuplicates = BooleanVar()
        self.__enableDuplicates.set(False)
        
        # Add menu for update check
        self.create_menu()
        
        self.__connected = False        
        self.__connectedLabelIndicator = None
        
        self.__tracks = ['', '', '']
        self.__trackOneEntry = None
        self.__trackTwoEntry = None
        self.__trackThreeEntry = None        
        
        self.__msr = None
        self.__db_conn = None
        self.__db_cursor = None
        
        # Initialize database
        self.init_database()
        
        self.build_main_window()
        
    def create_menu(self):
        """Create the application menu."""
        menubar = Menu(root)
        
        # File menu
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.on_exit)
        
        # Help menu
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="Check for Updates", command=self.check_for_updates)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.show_about)
        
        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        root.config(menu=menubar)
    
    def show_about(self):
        """Show about dialog with version information."""
        from version import get_version, get_version_info
        info = get_version_info()
        messagebox.showinfo(
            "About",
            f"MSR605 Reader/Writer\n"
            f"Version: {get_version()}\n"
            f"© 2024 MSR605 Project"
        )
    
    def check_for_updates(self):
        """Check for application updates."""
        from version import get_version as get_current_version
        current_version = get_current_version()
        check_for_updates(parent=root, current_version=current_version)
    
    def erase_card(self):
        """Erase all tracks on the card using the MSR605 device."""
        if not self.__msr or not self.__connected:
            showerror("Error", "MSR605 is not connected")
            return
            
        try:
            # Confirm before erasing
            if not askyesno("Confirm Erase", "This will erase ALL data on the card. Are you sure?"):
                return
                
            # Erase all three tracks
            for i in range(3):
                try:
                    self.__msr.erase_track(i + 1)
                except cardReaderExceptions.CardEraseError as e:
                    showerror("Erase Error", f"Failed to erase track {i+1}: {str(e)}")
                    return
            
            # Clear the track data in memory and UI
            self.__tracks = ['', '', '']
            self.__update_track_entries()
            
            showinfo("Success", "Card erased successfully!")
            
        except Exception as e:
            showerror("Error", f"Failed to erase card: {str(e)}")
    
    def write_card(self):
        """Write data to a card using the MSR605 device."""
        if not self.__msr or not self.__connected:
            showerror("Error", "MSR605 is not connected")
            return
            
        # Get the current track data from the UI
        self.__tracks = [
            self.__trackOneEntry.get("1.0", END).strip(),
            self.__trackTwoEntry.get("1.0", END).strip(),
            self.__trackThreeEntry.get("1.0", END).strip()
        ]
        
        if not any(self.__tracks):
            showerror("Error", "No track data to write. Please enter data in at least one track.")
            return
            
        try:
            # Confirm before writing
            if not askyesno("Confirm Write", "This will overwrite the card data. Are you sure?"):
                return
                
            # Write each track that has data
            for i, track_data in enumerate(self.__tracks):
                if track_data:  # Only write if there's data for this track
                    try:
                        self.__msr.write_track(i + 1, track_data)
                    except cardReaderExceptions.CardWriteError as e:
                        showerror("Write Error", f"Failed to write track {i+1}: {str(e)}")
                        return
            
            showinfo("Success", "Card written successfully!")
            
        except Exception as e:
            showerror("Error", f"Failed to write card: {str(e)}")
    
    def show_advanced_functions(self):
        """Show the advanced functions window with card data."""
        if not hasattr(self, '_GUI__tracks') or not any(self.__tracks):
            showerror("Error", "No track data available. Please read a card first.")
            return
            
        if not hasattr(self, '_advanced_window') or not self._advanced_window.winfo_exists():
            self._advanced_window = Toplevel(self)
            self._advanced_window.title("Advanced Card Functions")
            
            # Set window size and position
            window_width = 900
            window_height = 800
            screen_width = self._advanced_window.winfo_screenwidth()
            screen_height = self._advanced_window.winfo_screenheight()
            center_x = int(screen_width/2 - window_width/2)
            center_y = int(screen_height/2 - window_height/2)
            self._advanced_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
            
            # Create and pack the advanced functions frame
            self.advanced_frame = AdvancedFunctionsFrame(self._advanced_window, tracks=self.__tracks)
            self.advanced_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Add a close button at the bottom
            ttk.Button(
                self._advanced_window,
                text="Close",
                command=self._advanced_window.destroy
            ).pack(pady=10)
            
            # Handle window close
            self._advanced_window.protocol("WM_DELETE_WINDOW", self._advanced_window.destroy)
        else:
            # Update track data if window already exists
            self.advanced_frame.set_tracks(self.__tracks)
            self._advanced_window.lift()
            self._advanced_window.focus_force()
    
    def read_card(self, max_retries: int = 2):
        """
        Read data from a card using the MSR605 device.
        
        Args:
            max_retries: Maximum number of retry attempts for reading each track
        """
        if not hasattr(self, '_GUI__msr') or not self.__connected:
            showerror("Error", "MSR605 is not connected")
            return
        
        def clean_track_data(track_data: str) -> str:
            """Clean and validate track data."""
            if not track_data:
                return ''
                
            # Remove any non-printable characters
            cleaned = ''.join(char for char in track_data if 32 <= ord(char) <= 126)
            
            # Check for common error patterns
            error_patterns = [
                'READ ERROR',
                'ESCAPE(',
                'ERROR',
                'FAILED'
            ]
            
            if any(pattern in cleaned.upper() for pattern in error_patterns):
                return ''
                
            return cleaned
            
        try:
            print("\nATTEMPTING TO READ FROM CARD (SWIPE NOW)")
            
            # Reset track data
            self.__tracks = ['', '', '']
            read_success = False
            
            try:
                # Try to read all tracks at once first
                for attempt in range(max_retries + 1):
                    try:
                        tracks = self.__msr.read_card()
                        if isinstance(tracks, (list, tuple)) and len(tracks) == 3:
                            self.__tracks = [
                                clean_track_data(str(track) if track is not None else '')
                                for track in tracks
                            ]
                            if any(self.__tracks):  # If any track has data
                                read_success = True
                                break
                    except (cardReaderExceptions.CardReadError, Exception) as e:
                        if attempt == max_retries:
                            print(f"Final attempt failed: {str(e)}")
                            raise
                        time.sleep(0.5)  # Small delay before retry
                
                # If reading all tracks failed or returned no data, try individual tracks
                if not read_success:
                    print("Reading all tracks at once failed, trying individual tracks...")
                    for i in range(3):
                        for attempt in range(max_retries + 1):
                            try:
                                track_data = self.__msr.read_track(i + 1)
                                cleaned_data = clean_track_data(str(track_data) if track_data is not None else '')
                                if cleaned_data:  # Only update if we got valid data
                                    self.__tracks[i] = cleaned_data
                                    read_success = True
                                break  # Move to next track if successful
                            except (cardReaderExceptions.CardReadError, AttributeError) as e:
                                if attempt == max_retries:
                                    self.__tracks[i] = ''  # Clear track on final failure
                                    print(f"Failed to read track {i+1}: {str(e)}")
                                time.sleep(0.5)  # Small delay before retry
                            
            except Exception as e:
                error_msg = f"Error reading card: {str(e)}"
                print(error_msg)
                self.exception_error_reset("Read Error", error_msg)
                return
            
            # Update the UI with the read data
            self.__update_track_entries()
            
            # Show appropriate status message
            if read_success:
                showinfo("Success", "Card read successfully!")
            else:
                showerror("Error", "Failed to read card data. Please try again.")
            
            # Save to database if auto-save is enabled and we have some data
            if self.__autoSaveDatabase.get() and any(self.__tracks):
                self.__save_to_database()
                
            # Show success message if at least one track was read successfully
            if any(track and not str(track).startswith("Error") for track in self.__tracks):
                showinfo("Success", "Card read successfully!")
            else:
                showerror("Error", "Failed to read any track data from the card")
                
        except Exception as e:
            showerror("Error", f"Failed to read card: {str(e)}")
            # Reset tracks on error
            self.__tracks = ['', '', '']
            self.__update_track_entries()
    
    def __update_track_entries(self):
        """Update the track entry fields with the current track data."""
        for entry, data in zip([self.__trackOneEntry, self.__trackTwoEntry, self.__trackThreeEntry], self.__tracks):
            entry.delete(1.0, END)
            entry.insert(1.0, data)
    
    def __save_to_database(self):
        """Save the current track data to the database."""
        try:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            self.__db_cursor.execute(
                """
                INSERT INTO card_reads (timestamp, track1, track2, track3)
                VALUES (?, ?, ?, ?)
                """,
                (timestamp, self.__tracks[0], self.__tracks[1], self.__tracks[2])
            )
            self.__db_conn.commit()
        except Exception as e:
            showerror("Database Error", f"Failed to save to database: {str(e)}")
    
    def coercivity_change(self):
        """Handle coercivity radio button changes."""
        if not self.__msr or not self.__connected:
            return
            
        try:
            if self.__coercivityRadioBtnValue.get() == 'hi':
                self.__msr.set_hi_coercivity()
            else:
                self.__msr.set_lo_coercivity()
        except Exception as e:
            showerror("Error", f"Failed to change coercivity: {str(e)}")
    
    def connect_to_msr605(self):
        """Connect to the MSR605 device."""
        try:
            # Initialize the MSR605 reader
            self.__msr = CardReader()
            
            # Verify the connection was successful
            if not hasattr(self.__msr, '_CardReader__serialConn') or not self.__msr._CardReader__serialConn.is_open:
                raise ConnectionError("Failed to establish serial connection to MSR605")
                
            self.__connected = True
            self.__connectedLabelIndicator.config(text="MSR605 IS CONNECTED", fg='green')
            showinfo("Success", "Successfully connected to MSR605 device")
            
            # Reset the device to ensure clean state
            self.reset()
            
        except Exception as e:
            self.__connected = False
            self.__msr = None  # Ensure __msr is None if connection fails
            self.__connectedLabelIndicator.config(text="MSR605 CONNECTION FAILED", fg='red')
            showerror("Connection Error", f"Failed to connect to MSR605: {str(e)}")
    
    def exception_error_reset(self, title, error):
        """Handle errors during decryption and reset the UI state."""
        showerror(title, str(error))
        # Reset any necessary UI elements here if needed
        self.__tracks = ['', '', '']
        self.__update_track_entries()
    
    def close_connection(self):
        """Close the connection to the MSR605 device."""
        try:
            if hasattr(self, '_GUI__msr') and self.__msr is not None:
                try:
                    # Try to close the connection gracefully
                    if hasattr(self.__msr, 'close_serial_connection'):
                        self.__msr.close_serial_connection()
                    elif hasattr(self.__msr, 'close'):
                        self.__msr.close()
                    
                    self.__connected = False
                    self.__connectedLabelIndicator.config(text="MSR605 IS DISCONNECTED", fg='red')
                    showinfo("Success", "Successfully disconnected from MSR605 device")
                except Exception as e:
                    showerror("Error", f"Error while disconnecting: {str(e)}")
                finally:
                    self.__msr = None
                    self.__connected = False
            else:
                # If we get here, there was no active connection
                self.__connected = False
                self.__connectedLabelIndicator.config(text="MSR605 IS DISCONNECTED", fg='red')
        except Exception as e:
            # Handle any unexpected errors
            showerror("Error", f"Unexpected error while disconnecting: {str(e)}")
        finally:
            # Ensure these are always set on exit
            self.__connected = False
            if hasattr(self, '_GUI__connectedLabelIndicator'):
                self.__connectedLabelIndicator.config(text="MSR605 IS DISCONNECTED", fg='red')
        # No need to show a message when there's no active connection
        # This prevents the "No active connection to close" message
    
    def reset(self):
        """Reset the MSR605 device."""
        if self.__msr and self.__connected:
            try:
                self.__msr.reset()
                showinfo("Success", "MSR605 has been reset")
            except Exception as e:
                showerror("Error", f"Failed to reset MSR605: {str(e)}")
        else:
            showerror("Error", "MSR605 is not connected")
    
    def init_database(self):
        try:
            # Set up database path in user's documents folder
            db_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'MSR605')
            
            # Create database directory if it doesn't exist
            if not os.path.exists(db_dir):
                os.makedirs(db_dir)
            
            # Full path to database file
            db_path = os.path.join(db_dir, 'cardDatabase.db')
            
            # Initialize database connection
            self.__db_conn = sqlite3.connect(db_path)
            self.__db_cursor = self.__db_conn.cursor()
            
            # Create table if it doesn't exist
            self.__db_cursor.execute('''CREATE TABLE IF NOT EXISTS cards
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                     trackOne TEXT,
                                     trackTwo TEXT,
                                     trackThree TEXT,
                                     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
            self.__db_conn.commit()
            
            print(f"Database initialized at: {db_path}")
            if hasattr(self, 'status_var'):
                self.status_var.set(f'Database: Connected ({db_path})')
    
        except sqlite3.Error as e:
            showerror("Database Error", f"Failed to initialize database: {str(e)}")
        except OSError as e:
            showerror("File System Error", f"Failed to create database directory: {str(e)}")
        except Exception as e:
            showerror("Error", f"An unexpected error occurred: {str(e)}")
        

        
    def show_about(self):
        from about import About
        About.show_about(self.master)
    
    def show_help(self):
        help_text = """MSR605 Card Reader/Writer Help

Basic Operations:
1. Connect to MSR605 using the 'Connect' button
2. Set the appropriate coercivity (HI-CO or LOW-CO)
3. Use the Read/Write/Erase buttons to manage cards
4. Use Decode to view parsed card data

Database:
- Enable 'Autosave' to automatically save read cards
- View saved cards in the database viewer

For more information, visit:
https://github.com/Nsfr750/MSR605"""
        showinfo("Help", help_text)
    
    def show_sponsor(self):
        Sponsor(self.master).show_sponsor()

    def export_database_to_csv(self):
        try:
            # Ask user for save location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Export Database to CSV"
            )
            
            if not file_path:
                return  # User cancelled

            # Get all records
            self.__db_cursor.execute('SELECT * FROM cards')
            rows = self.__db_cursor.fetchall()

            # Get column names
            self.__db_cursor.execute('PRAGMA table_info(cards)')
            columns = [col[1] for col in self.__db_cursor.fetchall()]

            # Write to CSV
            with open(file_path, 'w', newline='') as csv_file:
                import csv
                writer = csv.writer(csv_file)
                writer.writerow(columns)  # Write header
                writer.writerows(rows)    # Write data

            showinfo("Export Successful", f"Database exported to {file_path}")

        except sqlite3.Error as e:
            showerror("Database Error", f"Failed to export database: {str(e)}")
        except Exception as e:
            showerror("Export Error", f"Failed to export: {str(e)}")

    def main_window_menu(self):
           
        m = Menu(root)
    
        fileMenu = Menu(m, tearoff=0)
        fileMenu.add("command", label="Exit", command=self.on_exit)
        m.add("cascade", menu=fileMenu, label="File")
        
        databaseMenu = Menu(m, tearoff=0)
        databaseMenu.add("command", label="View Database", command=self.view_database)
        databaseMenu.add("command", label="Export to CSV", command=self.export_database_to_csv)
        databaseMenu.add("separator")
        databaseMenu.add("checkbutton", label="Autosave Read Cards", onvalue=True, offvalue=False, variable=self.__autoSaveDatabase)
        databaseMenu.add("checkbutton", label="Save Duplicate Cards", onvalue=True, offvalue=False, variable=self.__enableDuplicates)
        m.add("cascade", menu=databaseMenu, label="Database")
        
        helpMenu = Menu(m, tearoff=0)
        helpMenu.add("command", label="Help Contents", command=self.show_help)
        helpMenu.add("separator")
        helpMenu.add("command", label="About", command=self.show_about)
        m.add("cascade", menu=helpMenu, label="Help")
        
        sponsorMenu = Menu(m, tearoff=0)
        sponsorMenu.add("command", label="Support Project", command=self.show_sponsor)
        m.add("cascade", menu=sponsorMenu, label="Sponsor")
        
        root.configure(menu=m)
        
        
        
    def build_main_window(self):
             
           
        #Calls main Window Menu along with a .configure -> Shows the menu
        m = self.main_window_menu()

        # Use root as the parent for tracks and buttons (revert change)
        tracks = Frame(root)
        tracks.pack(side=LEFT)

        # --- STATUS BAR ---
        self.status_var = StringVar()
        self.status_var.set('Database: Connecting...')
        self.status_bar = Label(root, textvariable=self.status_var, bd=1, relief=SUNKEN, anchor=W)
        self.status_bar.pack(side=BOTTOM, fill=X)

        # Track One
        trackOneFrame = Frame(tracks, padx=10, pady=10)
        trackOneFrame.grid(row=0, column=0)
        Label(trackOneFrame, text="Track 1", padx=10, pady=10).pack(side=LEFT)
        self.__trackOneEntry = Text(trackOneFrame, bd=1, width=50, height=3)
        self.__trackOneEntry.pack(side=RIGHT)

        # Track Two
        trackTwoFrame = Frame(tracks, padx=10, pady=10)
        trackTwoFrame.grid(row=1, column=0)
        Label(trackTwoFrame, text="Track 2", padx=10, pady=10).pack(side=LEFT)
        self.__trackTwoEntry = Text(trackTwoFrame, bd=1, width=50, height=3)
        self.__trackTwoEntry.pack(side=RIGHT)

        # Track Three
        trackThreeFrame = Frame(tracks, padx=10, pady=10)
        trackThreeFrame.grid(row=2, column=0)
        Label(trackThreeFrame, text="Track 3", padx=10, pady=10).pack(side=LEFT)
        self.__trackThreeEntry = Text(trackThreeFrame, bd=1, width=50, height=3)
        self.__trackThreeEntry.pack(side=RIGHT)

        # Displays if you're connected to the MSR605
        self.__connectedLabelIndicator = Label(tracks, text="MSR605 IS NOT CONNECTED", fg='red', padx=10, pady=10, font=('Helvetica', 14, 'underline'))
        self.__connectedLabelIndicator.grid(row=3, column=0)

        Button(tracks, text="Connect to MSR605", command=self.connect_to_msr605).grid(row=4, column=0)
        Button(tracks, text="Close connection to MSR605", command=self.close_connection).grid(row=5, column=0)
        Button(tracks, text="Reset MSR605", command=self.reset).grid(row=6, column=0)

        buttons = Frame(root)
        buttons.pack(side=RIGHT, fill=Y)

        # Coercivity Radio Buttons (remains at top)
        coercivityRadioButtons = Frame(buttons, padx=10, pady=10)
        coercivityRadioButtons.pack(side=TOP, padx=20, anchor=N)
        Label(coercivityRadioButtons, text="SET COERCIVITY", padx=10, pady=10, font=('Helvetica', 10, 'underline')).pack(side=TOP)
        Radiobutton(coercivityRadioButtons, text="HI-CO", variable=self.__coercivityRadioBtnValue, value="hi", command=self.coercivity_change).pack(side=TOP)
        Radiobutton(coercivityRadioButtons, text="LOW-CO", variable=self.__coercivityRadioBtnValue, value="low", command=self.coercivity_change).pack(side=TOP)

        # Button columns for better layout
        buttonColumns = Frame(buttons)
        buttonColumns.pack(side=TOP, fill=BOTH, expand=True)

        # Column 0: Read/Write/Erase, LED
        col0 = Frame(buttonColumns)
        col0.grid(row=0, column=0, sticky=N)
        readWriteEraseButtons = Frame(col0, padx=10, pady=10)
        readWriteEraseButtons.pack(side=TOP, padx=10, pady=10, anchor=N)
        Label(readWriteEraseButtons, text="READ/WRITE\n/ERASE CARDS", padx=10, pady=10, font=('Helvetica', 10, 'underline')).pack(side=TOP)
        Button(readWriteEraseButtons, text="READ CARD", command=self.read_card).pack(side=TOP)
        Button(readWriteEraseButtons, text="ADVANCED FUNCTIONS", command=self.show_advanced_functions).pack(side=TOP)
        Button(readWriteEraseButtons, text="DECRYPT CARD", command=self.decrypt_card).pack(side=TOP)
        Button(readWriteEraseButtons, text="WRITE CARD", command=self.write_card).pack(side=TOP)
        Button(readWriteEraseButtons, text="ERASE CARD", command=self.erase_card).pack(side=TOP)

        ledButtons = Frame(col0, padx=10, pady=10)
        ledButtons.pack(side=TOP, padx=10, pady=10, anchor=N)
        Label(ledButtons, text="LED OPTIONS", padx=10, pady=10, font=('Helvetica', 10, 'underline')).pack(side=TOP)
        Button(ledButtons, text="ALL ON", command=lambda: self.led_change("on")).pack(side=TOP)
        Button(ledButtons, text="ALL OFF", command=lambda: self.led_change("off")).pack(side=TOP)
        Button(ledButtons, text="GREEN ON", command=lambda: self.led_change("green")).pack(side=TOP)
        Button(ledButtons, text="YELLOW ON", command=lambda: self.led_change("yellow")).pack(side=TOP)
        Button(ledButtons, text="RED ON", command=lambda: self.led_change("red")).pack(side=TOP)

        # Column 1: Tests, Advanced Tools
        col1 = Frame(buttonColumns)
        col1.grid(row=0, column=1, sticky=N)
        testButtons = Frame(col1, padx=10, pady=10)
        testButtons.pack(side=TOP, padx=10, pady=10, anchor=N)
        Label(testButtons, text="MSR605 TESTS", padx=10, pady=10, font=('Helvetica', 10, 'underline')).pack(side=TOP)
        Button(testButtons, text="COMMUNICATION TEST", command=self.communication_test).pack(side=TOP)
        Button(testButtons, text="SENSOR TEST", command=self.sensor_test).pack(side=TOP)
        Button(testButtons, text="RAM TEST", command=self.ram_test).pack(side=TOP)

        advancedFrame = Frame(col1, padx=10, pady=10)
        advancedFrame.pack(side=TOP, padx=10, pady=10, anchor=N)
        Label(advancedFrame, text="ADVANCED TRACK TOOLS", padx=10, pady=10, font=('Helvetica', 10, 'underline')).pack(side=TOP)
        Button(advancedFrame, text="Set Leading Zero", command=self.set_leading_zero_gui).pack(side=TOP, fill=X)
        Button(advancedFrame, text="Clear Leading Zero", command=lambda: self.set_leading_zero_gui(enable=False)).pack(side=TOP, fill=X)
        Button(advancedFrame, text="Check Leading Zero", command=self.check_leading_zero_gui).pack(side=TOP, fill=X)
        Button(advancedFrame, text="Select BPI", command=self.select_bpi_gui).pack(side=TOP, fill=X)
        Button(advancedFrame, text="Set BPC", command=self.set_bpc_gui).pack(side=TOP, fill=X)
        Button(advancedFrame, text="Read Raw Data", command=self.read_raw_data_gui).pack(side=TOP, fill=X)
        Button(advancedFrame, text="Write Raw Data", command=self.write_raw_data_gui).pack(side=TOP, fill=X)

    def communication_test(self):
        if (self.__connected == False or self.__msr == None):
            showerror("Connect Error", "The MSR605 is not connected")
            return None
        
        try:
            self.__msr.communication_test()
        except cardReaderExceptions.CommunicationTestError as e:
            self.exception_error_reset("Communication Test Error", e)
            print(e)
            return None
        else:
            showinfo("Communication Test", "Communication between your computer and the MSR605 is good")
        
    def decrypt_card(self):
        """Decrypt the card data using the decrypt.py module."""
        output = io.StringIO()
        old_stdout = sys.stdout
        try:
            sys.stdout = output
            tracks = self.__msr.read_card()
        except cardReaderExceptions.CardReadError as e:
            sys.stdout = old_stdout
            self.exception_error_reset("Decode Error", e)
            print(e)
            showerror("Decode Error", f"Failed to decode card: {e}")
            return None
        except Exception as e:
            sys.stdout = old_stdout
            print(e)
            showerror("Decode Error", f"Unexpected error: {e}")
            return None
        finally:
            sys.stdout = old_stdout
        decoded_data = output.getvalue()
        if not decoded_data.strip():
            showwarning("Decode Warning", "No card data was decoded. Please try again.")
            return
        # Parse the tracks using parser.py
        parsed = parser.parse_all_tracks(tracks)
        info = []
        if parsed['track1']:
            t1 = parsed['track1']
            details = [
                f"Track 1:",
                f"  Card Number : {t1.get('card_number','')}",
                f"  Name        : {t1.get('name','')}",
                f"  Expiration  : {t1.get('expiration','')}",
                f"  Raw         : {t1.get('raw','')}",
            ]
            if 'error' in t1:
                details.append(f"  Error       : {t1['error']}")
            info.append('\n'.join(details))
        if parsed['track2']:
            t2 = parsed['track2']
            details = [
                f"Track 2:",
                f"  Card Number : {t2.get('card_number','')}",
                f"  Expiration  : {t2.get('expiration','')}",
                f"  Service Code: {t2.get('service_code','')}",
                f"  Raw         : {t2.get('raw','')}",
            ]
            if 'error' in t2:
                details.append(f"  Error       : {t2['error']}")
            info.append('\n'.join(details))
        if parsed['track3']:
            t3 = parsed['track3']
            details = [
                f"Track 3:",
                f"  Raw         : {t3.get('raw','')}",
                f"  Hex         : {t3.get('hex','')}",
                f"  Length      : {t3.get('length','')}",
                f"  Printable   : {t3.get('printable','')}",
            ]
            if 'error' in t3:
                details.append(f"  Error       : {t3['error']}")
            info.append('\n'.join(details))
        showinfo("Decoded Card Data", '\n\n'.join(info))


            
    def set_leading_zero_gui(self, enable=True):
        if self.__connected == False or self.__msr == None:
            showerror("Connect Error", "The MSR605 is not connected")
            return
        track = simpledialog.askinteger("Set Leading Zero", "Enter track (1, 2, or 3):", minvalue=1, maxvalue=3)
        if track is None:
            return
        try:
            self.__msr.set_leading_zero(track=track, enable=enable)
            showinfo("Success", f"Leading zero {'set' if enable else 'cleared'} for track {track}.")
        except Exception as e:
            showerror("Error", str(e))

    def check_leading_zero_gui(self):
        if self.__connected == False or self.__msr == None:
            showerror("Connect Error", "The MSR605 is not connected")
            return
        track = simpledialog.askinteger("Check Leading Zero", "Enter track (1, 2, or 3):", minvalue=1, maxvalue=3)
        if track is None:
            return
        try:
            result = self.__msr.check_leading_zero(track=track)
            showinfo("Leading Zero", f"Track {track}: {'SET' if result else 'NOT SET'}")
        except Exception as e:
            showerror("Error", str(e))

    def select_bpi_gui(self):
        if self.__connected == False or self.__msr == None:
            showerror("Connect Error", "The MSR605 is not connected")
            return
        track = simpledialog.askinteger("Select BPI", "Enter track (1, 2, or 3):", minvalue=1, maxvalue=3)
        if track is None:
            return
        bpi = simpledialog.askinteger("Select BPI", "Enter BPI (75 or 210):", minvalue=75, maxvalue=210)
        if bpi not in (75, 210):
            showerror("Error", "BPI must be 75 or 210")
            return
        try:
            self.__msr.select_bpi(track=track, bpi=bpi)
            showinfo("Success", f"BPI {bpi} set for track {track}.")
        except Exception as e:
            showerror("Error", str(e))

    def set_bpc_gui(self):
        if self.__connected == False or self.__msr == None:
            showerror("Connect Error", "The MSR605 is not connected")
            return
        track = simpledialog.askinteger("Set BPC", "Enter track (1, 2, or 3):", minvalue=1, maxvalue=3)
        if track is None:
            return
        bpc = simpledialog.askinteger("Set BPC", "Enter BPC (5, 7, or 8):", minvalue=5, maxvalue=8)
        if bpc not in (5, 7, 8):
            showerror("Error", "BPC must be 5, 7, or 8")
            return
        try:
            self.__msr.set_bpc(track=track, bpc=bpc)
            showinfo("Success", f"BPC {bpc} set for track {track}.")
        except Exception as e:
            showerror("Error", str(e))

    def read_raw_data_gui(self):
        if self.__connected == False or self.__msr == None:
            showerror("Connect Error", "The MSR605 is not connected")
            return
        track = simpledialog.askinteger("Read Raw Data", "Enter track (1, 2, or 3):", minvalue=1, maxvalue=3)
        if track is None:
            return
        try:
            data = self.__msr.read_raw_data(track=track)
            showinfo("Raw Data", f"Track {track} raw data:\n{data}")
        except Exception as e:
            showerror("Error", str(e))

    def write_raw_data_gui(self):
        if self.__connected == False or self.__msr == None:
            showerror("Connect Error", "The MSR605 is not connected")
            return
        track = simpledialog.askinteger("Write Raw Data", "Enter track (1, 2, or 3):", minvalue=1, maxvalue=3)
        if track is None:
            return
        data = simpledialog.askstring("Write Raw Data", "Enter raw data (as ASCII string):")
        if data is None:
            return
        try:
            self.__msr.write_raw_data(track=track, data=data.encode())
            showinfo("Success", f"Raw data written to track {track}.")
        except Exception as e:
            showerror("Error", str(e))

    def ram_test(self):
        if (self.__connected == False or self.__msr == None):
            showerror("Connect Error", "The MSR605 is not connected")
            return None
        
        try:
            self.__msr.ram_test()
        
        except cardReaderExceptions.RamTestError as e :
            self.exception_error_reset("Ram Test Error", e)
            print (e)
            return None
        
        else:
            showinfo("Ram Test", "MSR605 Ram is good")
            
    def sensor_test(self):
        if (self.__connected == False or self.__msr == None):
            showerror("Connect Error", "The MSR605 is not connected")
            return None
        
        showinfo("Sensor Test", "Please swipe card after hitting OK")
        
        try:
            self.__msr.sensor_test()
        
        except cardReaderExceptions.SensorTestError as e :
            self.exception_error_reset("Sensor Test Error", e)
            print (e)
            return None
        
        else:
            showinfo("Sensor Test", "MSR605 Sensor's are good")
    

    def view_database(self):
        try:
            self.__db_cursor.execute("""SELECT id, trackOne, trackTwo, trackThree, timestamp FROM cards ORDER BY id DESC""")
            result = self.__db_cursor.fetchall()
            
            if (len(result) == 0):
                showinfo("Database", "Database is empty")
                return None
            
            databaseWindow = Toplevel()
            databaseWindow.title("Database Viewer")
            databaseWindow.minsize(800,600)
            
            # Main container frame with padding
            mainFrame = Frame(databaseWindow, padx=10, pady=10)
            mainFrame.pack(fill=BOTH, expand=True)
            
            # Header label
            Label(mainFrame, text="Stored Cards", font=("Helvetica", 14, "bold"), pady=10).pack()
            
            # Database Frame with Treeview
            databaseFrame = Frame(mainFrame)
            databaseFrame.pack(fill=BOTH, expand=True)
            
            # Create Treeview with columns
            tree = ttk.Treeview(databaseFrame)
            tree["columns"] = ("ID", "Track 1", "Track 2", "Track 3", "Timestamp")
            
            # Configure columns
            tree.column("#0", width=0, stretch=NO)  # Hide first column
            tree.column("ID", width=50, anchor=CENTER)
            tree.column("Track 1", width=200, anchor=W)
            tree.column("Track 2", width=200, anchor=W)
            tree.column("Track 3", width=200, anchor=W)
            tree.column("Timestamp", width=150, anchor=W)
            
            # Configure headings
            tree.heading("ID", text="ID")
            tree.heading("Track 1", text="Track 1")
            tree.heading("Track 2", text="Track 2")
            tree.heading("Track 3", text="Track 3")
            tree.heading("Timestamp", text="Timestamp")
            
            # Add vertical scrollbar
            vsb = ttk.Scrollbar(databaseFrame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=vsb.set)
            
            # Add horizontal scrollbar
            hsb = ttk.Scrollbar(databaseFrame, orient="horizontal", command=tree.xview)
            tree.configure(xscrollcommand=hsb.set)
            
            # Grid layout for scrollbars
            tree.grid(row=0, column=0, sticky=NSEW)
            vsb.grid(row=0, column=1, sticky=NS)
            hsb.grid(row=1, column=0, sticky=EW)
            
            # Configure grid weights
            databaseFrame.grid_rowconfigure(0, weight=1)
            databaseFrame.grid_columnconfigure(0, weight=1)
            
            # Insert data
            for row in result:
                tree.insert("", "end", values=row)
            
            # Add info label
            Label(mainFrame, text=f"Total records: {len(result)}", pady=5).pack()
            
        except sqlite3.Error as e:
            showerror("Database Error", f"Failed to view database: {str(e)}")
        except Exception as e:
            showerror("Error", f"An error occurred: {str(e)}")       
        
    def on_exit(self):
        # Close database connection
        if self.__db_conn:
            try:
                self.__db_conn.close()
            except sqlite3.Error:
                pass
        
        # Close MSR605 connection
        if (self.__connected == True or self.__msr != None):
            self.close_connection()
        
        showinfo("Bye Bye")
        root.destroy()


def main():
    """Main entry point for the application."""
    global root
    root = tk.Tk()
    root.title(f"MSR605 Reader/Writer {get_version()}")
    root.minsize(700, 600)
    
    def check_updates():
        """Check for application updates."""
        try:
            from version import get_version as get_current_version
            current_version = get_current_version()
            check_for_updates(parent=root, current_version=current_version)
        except Exception as e:
            print(f"Error checking for updates: {e}")
    
    # Check for updates after the main window is initialized
    root.after(1000, check_updates)
    
    gui = GUI(root)
    root.protocol("WM_DELETE_WINDOW", gui.on_exit)
    root.mainloop()


if __name__ == "__main__":
    from version import get_version
    main()

if __name__ == "__main__":
    main()