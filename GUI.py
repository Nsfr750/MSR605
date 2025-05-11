#!/usr/bin/env python3

import tkinter as tk
import sys, time, cardReaderExceptions, cardReader
import os
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from tkinter import filedialog, simpledialog
import sqlite3

# Sponsor Class
class Sponsor:
    def show_sponsor_window(self):
        sponsor_root = Toplevel()
        sponsor_root.geometry("300x200")
        sponsor_root.title("Sponsor")

        title_label = tk.Label(sponsor_root, text="Support Us", font=("Arial", 16))
        title_label.pack(pady=10)

        def open_patreon():
            import webbrowser
            webbrowser.open("https://www.patreon.com/Nsfr750")

        def open_github():
            import webbrowser
            webbrowser.open("https://github.com/sponsors/Nsfr750")

        def open_discord():
            import webbrowser
            webbrowser.open("https://discord.gg/BvvkUEP9")

        def open_paypal():
            import webbrowser
            webbrowser.open("https://paypal.me/3dmega")

        # Create and place buttons
        patreon_button = tk.Button(sponsor_root, text="Join the Patreon!", command=open_patreon)
        patreon_button.pack(pady=5)

        github_button = tk.Button(sponsor_root, text="GitHub", command=open_github)
        github_button.pack(pady=5)

        discord_button = tk.Button(sponsor_root, text="Join on Discord", command=open_discord)
        discord_button.pack(pady=5)

        paypal_button = tk.Button(sponsor_root, text="Pay me a Coffee", command=open_paypal)
        paypal_button.pack(pady=5)

        sponsor_root.mainloop()

class GUI(Frame):    
    def __init__(self, parent):
        Frame.__init__(self, parent)


        
        self.__coercivityRadioBtnValue = StringVar()
        self.__coercivityRadioBtnValue.set('hi')
        
        self.__autoSaveDatabase = BooleanVar()
        self.__autoSaveDatabase.set(False)
        
        self.__enableDuplicates = BooleanVar()
        self.__enableDuplicates.set(False)
        
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
        about_text = """MSR605 Card Reader/Writer v2.0.1

A GUI application for reading, writing, and managing magnetic stripe cards.

Copyright 2025 Nsfr750
License: GNU General Public License v3"""
        showinfo("About", about_text)
    
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
        sponsor_text = """Support MSR605 Card Reader/Writer

If you find this software useful, consider:
- Contributing to the project on GitHub
- Reporting bugs and suggesting features
- Supporting the development through donations

Social Links

- [Patreon](https://www.patreon.com/Nsfr750)
- [GitHub](https://github.com/sponsors/Nsfr750)
- [Discord](https://discord.gg/BvvkUEP9)
- [Payapal](https://paypal.me/3dmega)"""
        showinfo("Sponsor", sponsor_text)
        Sponsor().show_sponsor_window()

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
        Button(readWriteEraseButtons, text="DECODE CARD", command=self.decode_card).pack(side=TOP)
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

    
           
    def connect_to_msr605(self):        
        if (self.__connected == True or self.__msr != None):
            showinfo('Connecting', 'Reconnecting to MSR605')
            self.close_connection()
        
        try:
            self.__msr = cardReader.CardReader()
        
        except cardReaderExceptions.MSR605ConnectError as e:
            self.__connected = False
            self.__connectedLabelIndicator.config(text = "MSR605 IS NOT CONNECTED", fg = 'red')
            showerror("Connect Error", e)
            print (e)
        
        except cardReaderExceptions.CommunicationTestError as e:
            self.__connected = False
            self.__connectedLabelIndicator.config(text = "MSR605 IS NOT CONNECTED", fg = 'red')
            showerror("Communication Error", e)            
            print (e)
        
        else:
            self.__connected = True
            self.__connectedLabelIndicator.config(text = "MSR605 IS CONNECTED", fg = 'green')
            showinfo('MSR605 Initialize', 'MSR605 Successfully Connected')
            self.init_database()
    
    
    def close_connection(self):
        if (self.__connected == True or self.__msr != None):
            self.__msr.close_serial_connection()
            self.__connected = False
            self.__connectedLabelIndicator.config(text = "MSR605 IS NOT CONNECTED", fg = 'red')
            self.__msr = None
        
        else:
            showinfo('Close Connection', 'MSR605 is not connected')
    
    def exception_error_reset(self, title, text):
        showerror(title, text)
        
        showinfo("Resetting", "Resetting MSR605 because of error")
        self.reset()
        
        
    def coercivity_change(self):
        if (self.__connected == False or self.__msr == None):
            showerror("Connect Error", "The MSR605 is not connected")
            return None
        
        rdbSelection = self.__coercivityRadioBtnValue.get()        
        
        try:
            if (rdbSelection == 'hi'):            
                self.__msr.set_hi_co()
            elif (rdbSelection == 'low'):
                self.__msr.set_low_co()
                
        except cardReaderExceptions.SetCoercivityError as e :
            self.exception_error_reset("Setting Coercivity Error", e)
            print (e)            
        
        else:
            showinfo("Setting Coercivity", "Coercivity has been set, now checking Coercivity ")
            
            try:
                coercivity = self.__msr.get_hi_or_low_co()
            except cardReaderExceptions.GetCoercivityError as e :
                self.exception_error_reset("Getting Coercivity Error", e)
                print (e)
            else:
                showinfo("Getting Coercivity", "Coercivity has been set to " + coercivity)
            
            
            
    def read_card(self):
        if (self.__connected == False or self.__msr == None):
            showerror("Connect Error", "The MSR605 is not connected")
            return None
            
        try:
            self.__tracks = self.__msr.read_card()
        except cardReaderExceptions.CardReadError as e :
            self.exception_error_reset("Connect Error", e)
            print (e)
            
            self.__trackOneEntry.delete(1.0, END)
            self.__trackTwoEntry.delete(1.0, END)
            self.__trackThreeEntry.delete(1.0, END)
            
            self.__trackOneEntry.insert(END, e.tracks[0])
            self.__trackTwoEntry.insert(END, e.tracks[1])
            self.__trackThreeEntry.insert(END, e.tracks[2])
            
            if (self.__autoSaveDatabase.get() == True):
                
                if (self.__enableDuplicates.get() == False):
                    
                    self.__db_cursor.execute("""SELECT * FROM cards WHERE trackOne=? AND trackTwo=? AND trackThree=?""", (self.__tracks[0], self.__tracks[1], self.__tracks[2]))
                
                    result = self.__db_cursor.fetchone()

                    if (result != None):
                        showinfo("Duplicate", "This card already exists in the Database, please enable Duplicates in the Database dropdown to add it")
                    
                    else:
                        self.__db_cursor.execute("""INSERT INTO cards(trackOne, trackTwo, trackThree) VALUES(?, ?, ?)""", (self.__tracks[0], self.__tracks[1], self.__tracks[2]))                    
                        self.__db_conn.commit()                
                else:                
                    self.__db_cursor.execute("""INSERT INTO cards(trackOne, trackTwo, trackThree) VALUES(?, ?, ?)""", (self.__tracks[0], self.__tracks[1], self.__tracks[2]))                    
                    self.__db_conn.commit()
            
            
            else:
                showinfo("Autosave to Database","Autosave is turned off in the Database menu dropdown, please \nselect it if you wish to store the cards that are read in")
            
            
            return None
    
        except cardReaderExceptions.StatusError as e :
            self.exception_error_reset("Connect Error", e)
            print (e)
            return None
        
        else:
            self.__trackOneEntry.delete(1.0, END)
            self.__trackTwoEntry.delete(1.0, END)
            self.__trackThreeEntry.delete(1.0, END)
            
            self.__trackOneEntry.insert(END, self.__tracks[0] if self.__tracks[0] is not None else "")
            self.__trackTwoEntry.insert(END, self.__tracks[1] if self.__tracks[1] is not None else "")
            self.__trackThreeEntry.insert(END, self.__tracks[2] if self.__tracks[2] is not None else "")
        
            if (self.__autoSaveDatabase.get() == True):
                
                if (self.__enableDuplicates.get() == False):
                    
                    self.__db_cursor.execute("""SELECT * FROM cards WHERE trackOne=? AND trackTwo=? AND trackThree=?""", (self.__tracks[0], self.__tracks[1], self.__tracks[2]))
                
                    result = self.__db_cursor.fetchone()
                    
                    if (result != None):
                        showinfo("Duplicate", "This card already exists in the Database, please enable Duplicates in the Database dropdown to add it")
                    
                    else:
                        self.__db_cursor.execute("""INSERT INTO cards(trackOne, trackTwo, trackThree) VALUES(?, ?, ?)""", (self.__tracks[0], self.__tracks[1], self.__tracks[2]))                    
                        self.__db_conn.commit()                
                else:                
                    self.__db_cursor.execute("""INSERT INTO cards(trackOne, trackTwo, trackThree) VALUES(?, ?, ?)""", (self.__tracks[0], self.__tracks[1], self.__tracks[2]))                    
                    self.__db_conn.commit()
            else:
                showinfo("Autosave to Database","Autosave is turned off in the Database menu dropdown, please \nselect it if you wish to store the cards that are read in")
            
                
    def write_card(self):
        if (self.__connected == False or self.__msr == None):
            showerror("Connect Error", "The MSR605 is not connected")
            return None
        
        tracks = [self.__trackOneEntry.get(1.0, END)[:-1], self.__trackTwoEntry.get(1.0, END)[:-1], self.__trackThreeEntry.get(1.0, END)[:-1]]

        showinfo("Swipe Card", "Please swipe card after hitting OK")
        
        try:        
            self.__tracks = self.__msr.write_card(tracks, True)
        
        except cardReaderExceptions.CardWriteError as  e :
            self.exception_error_reset("Write Error", e)
            print(e)
            return None
        
        except cardReaderExceptions.StatusError as e :
            self.exception_error_reset("Write Error", e)
            print(e)
            return None
        
        else:
            showinfo("Write", "Tracks have been written to the Card")
        
    def erase_card(self):
        if (self.__connected == False or self.__msr == None):
            showerror("Connect Error", "The MSR605 is not connected")
            return None
        
        showinfo("Erase Card", "Please swipe card after hitting OK")
        
        #
        #
        #CHECK THIS************
        #
        #
        try:
            self.__msr.erase_card(7) #all tracks are erased
        
        except cardReaderExceptions.EraseCardError as e :
            self.exception_error_reset("Erase Error", e)
            print (e)
            return None
        
        else:
            showinfo("Erase Card", "Successfully Erased Card")
            
            
    def led_change(self, whichLeds):
        if (self.__connected == False or self.__msr == None):
            showerror("Connect Error", "The MSR605 is not connected")
            return None
       
        if (whichLeds == "on"):
            self.__msr.led_on()
            showinfo("LED'S", "All LED's On")
            return None
            
        elif (whichLeds == "off"):
            self.__msr.led_off()
            showinfo("LED'S", "All LED's Off")
            return None
        
        elif (whichLeds == "green"):
            self.__msr.green_led_on()
            showinfo("LED'S", "Green LED On")
            return None
            
        elif (whichLeds == "yellow"):
            self.__msr.yellow_led_on()
            showinfo("LED'S", "Yellow LED On")
            return None
            
        elif (whichLeds == "red"):
            self.__msr.red_led_on()
            showinfo("LED'S", "Red LED On")
            return None
            
    def reset(self):
        if (self.__connected == False or self.__msr == None):
            showerror("Reset Error", "The MSR605 is not connected")
            return None
        
        self.__msr.reset()
        showinfo("Reset", "The MSR605 has been reset")
    
    def communication_test(self):
        if (self.__connected == False or self.__msr == None):
            showerror("Connect Error", "The MSR605 is not connected")
            return None
        
        try:
            self.__msr.communication_test()
        
        except cardReaderExceptions.CommunicationTestError as e :
            self.exception_error_reset("Communication Test Error", e)
            print (e)
            return None
        
        else:
            showinfo("Communication Test", "Communication between your computer and the MSR605 is good")
        
    def decode_card(self):
        if (self.__connected == False or self.__msr == None):
            showerror("Connect Error", "The MSR605 is not connected")
            return None

        import io
        import sys
        import parser
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
        
        
root = tk.Tk()
root.title("MSR605 Reader/Writer v2.0.1")
root.minsize(700,600)
gui = GUI(root)

root.protocol("WM_DELETE_WINDOW", gui.on_exit)
root.mainloop() 


# Launch the status message after 1 millisecond (when the window is loaded)
#root.after(1, update_status)