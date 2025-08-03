import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from selenium_assistant_functions import *

class IddaaFiksturApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mackolik Data Scraper Application")
        self.root.geometry("450x550")
        self.root.resizable(False, False)
        
        # Variables
        self.driver = None
        self.soup = None
        self.iddaa_ligleri_list = []
        self.sezon_list = []
        self.sezon_haftalari_list = []
        
        self.selected_lig = tk.StringVar()
        self.selected_sezon = tk.StringVar()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Mackolik Data Scraper", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Start button
        self.start_button = ttk.Button(main_frame, text="Initialize Scraper", 
                                      command=self.start_process, width=25)
        self.start_button.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Betting League Selection
        self.lig_frame = ttk.Frame(main_frame)
        self.lig_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(self.lig_frame, text="Betting League:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.lig_combo = ttk.Combobox(self.lig_frame, textvariable=self.selected_lig, 
                                     width=35, state="disabled")
        self.lig_combo.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.lig_combo.bind('<<ComboboxSelected>>', self.on_lig_selected)
        
        self.lig_select_button = ttk.Button(self.lig_frame, text="Select League", 
                                           command=self.select_lig, state="disabled")
        self.lig_select_button.grid(row=1, column=1, padx=(10, 0))
        
        # Season Selection
        self.sezon_frame = ttk.Frame(main_frame)
        self.sezon_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(self.sezon_frame, text="League Season:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.sezon_combo = ttk.Combobox(self.sezon_frame, textvariable=self.selected_sezon, 
                                       width=35, state="disabled")
        self.sezon_combo.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.sezon_combo.bind('<<ComboboxSelected>>', self.on_sezon_selected)
        
        self.sezon_select_button = ttk.Button(self.sezon_frame, text="Select Season", 
                                             command=self.select_sezon, state="disabled")
        self.sezon_select_button.grid(row=1, column=1, padx=(10, 0))
      
        
        # Extract Data button
        self.data_button = ttk.Button(main_frame, text="Extract Data", 
                                     command=self.get_data, state="disabled", width=25)
        self.data_button.grid(row=5, column=0, columnspan=2, pady=(20, 20))
        
        # Status
        self.status_label = ttk.Label(main_frame, text="Ready to start", foreground="green", 
                                     font=('Arial', 9))
        self.status_label.grid(row=6, column=0, columnspan=2)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Instructions label
        instructions = ttk.Label(main_frame, 
                               text="1. Initialize scraper\n2. Select betting league\n3. Select season\n4. Extract data",
                               font=('Arial', 8), foreground="gray", justify="left")
        instructions.grid(row=8, column=0, columnspan=2, pady=(15, 0))
        
        # Grid weights
        main_frame.columnconfigure(0, weight=1)
        self.lig_frame.columnconfigure(0, weight=1)
        self.sezon_frame.columnconfigure(0, weight=1)
        
    def update_status(self, message, color="black"):
        self.status_label.config(text=message, foreground=color)
        self.root.update()
        
    def start_progress(self):
        self.progress.start()
        
    def stop_progress(self):
        self.progress.stop()
        
    def start_process(self):
        def run():
            try:
                self.start_button.config(state="disabled")
                self.start_progress()
                self.update_status("Initializing Selenium WebDriver...", "blue")
                
                # Start Selenium operations
                driver = start_selenium()
                # driver = webdriver.Chrome()  # add your driver here
                self.driver = driver
                
                time.sleep(randomize_sleep_time(4))
                reklami_gec(driver)
                time.sleep(randomize_sleep_time(4))
                accept_cookies(driver, randomize_sleep_time(3))
                time.sleep(randomize_sleep_time(3))
                soup = get_current_soup(driver)
                self.soup = soup
                
                # Get betting leagues list
                self.iddaa_ligleri_list = get_iddia_ligleri_selection_list(soup)
                
                # Test data (use above lines in real code)
                # self.iddaa_ligleri_list = ["TURKEY Super League", "BULGARIA 1st League", "GERMANY Bundesliga"]
                
                self.lig_combo.config(state="readonly")
                self.lig_combo['values'] = self.iddaa_ligleri_list
                self.lig_select_button.config(state="normal")
                
                self.stop_progress()
                self.update_status("Please select a betting league", "green")
                
            except Exception as e:
                self.stop_progress()
                self.update_status(f"Error: {str(e)}", "red")
                messagebox.showerror("Error", f"Error initializing Selenium: {str(e)}")
                self.start_button.config(state="normal")
        
        threading.Thread(target=run, daemon=True).start()
    
    def on_lig_selected(self, event):
        if self.selected_lig.get():
            self.lig_select_button.config(state="normal")
    
    def select_lig(self):
        def run():
            try:
                self.lig_select_button.config(state="disabled")
                self.start_progress()
                self.update_status("Selecting league...", "blue")
                
                selection_iddia_lig = self.selected_lig.get()
                
                select_iddaa_ligi(self.driver, selection_iddia_lig)
                reklami_gec(self.driver, randomize_sleep_time(5))
                time.sleep(randomize_sleep_time(3))
                soup = get_current_soup(self.driver)
                time.sleep(randomize_sleep_time(4))
                self.sezon_list = get_sezon_selections(soup)
                
                # Test data
                # self.sezon_list = ["2023/2024", "2022/2023", "2021/2022"]
                
                self.sezon_combo.config(state="readonly")
                self.sezon_combo['values'] = self.sezon_list
                self.sezon_select_button.config(state="normal")
                
                self.stop_progress()
                self.update_status("Please select a season", "green")
                
            except Exception as e:
                self.stop_progress()
                self.update_status(f"Error: {str(e)}", "red")
                messagebox.showerror("Error", f"Error selecting league: {str(e)}")
                self.lig_select_button.config(state="normal")
        
        threading.Thread(target=run, daemon=True).start()
    
    def on_sezon_selected(self, event):
        if self.selected_sezon.get():
            self.sezon_select_button.config(state="normal")
    
    def select_sezon(self):
        def run():
            try:
                self.sezon_select_button.config(state="disabled")
                self.start_progress()
                self.update_status("Selecting season...", "blue")
                
                selection_season = self.selected_sezon.get()
                
                select_season(self.driver, selection_season)
                time.sleep(randomize_sleep_time(4))
                open_fikstur_page(self.driver, randomize_sleep_time(6))
                time.sleep(randomize_sleep_time(5))
                fikstur_page_soup = get_current_soup(self.driver)
                self.sezon_haftalari_list = get_sezon_weeks(fikstur_page_soup)
                
                self.data_button.config(state="normal")
                # Test data
                # self.sezon_haftalari_list = [
                #     "1 (23.07.2021 - 26.07.2021)",
                #     "2 (30.07.2021 - 02.08.2021)",
                #     "3 (06.08.2021 - 09.08.2021)"
                # ]
                self.stop_progress()
                self.update_status("Ready to extract data - click Extract Data button", "green")
                
                                                
            except Exception as e:
                self.stop_progress()
                self.update_status(f"Error: {str(e)}", "red")
                messagebox.showerror("Error", f"Error selecting season: {str(e)}")
                self.sezon_select_button.config(state="normal")
        
        threading.Thread(target=run, daemon=True).start()
        
    def get_data(self):
        def run():
            try:
                self.data_button.config(state="disabled")
                self.start_progress()
                self.update_status("Extracting data...", "blue")
                
                ###
                final_df = get_all_weeks_data(self.driver, self.sezon_haftalari_list)
                # Format date
                try:
                    self.update_status("Formatting dates...", "blue")
                    
                    # Check if Week and Date columns exist
                    if 'Hafta' in final_df.columns and 'Tarih' in final_df.columns:
                        # Apply format_date function
                        final_df['Tarih'] = final_df.apply(
                            lambda row: format_date(row['Tarih'], row['Hafta']), 
                            axis=1
                        )
                        print("Date format updated:")
                        print(final_df[['Tarih', 'Hafta']].head())
                    else:
                        print("Warning: 'Tarih' or 'Hafta' column not found. Date format not updated.")
                        
                except Exception as e:
                    print(f"Error updating date format: {e}")
                    print("Original date format will be preserved.")
                
                print("Processed final data:")
                print(final_df)
                try:
                    save_to_excel(final_df, self.selected_lig.get(), self.selected_sezon.get())
                except Exception as e:
                    print("An error occurred. Saving as CSV. Error:",e)
                    save_to_csv(final_df, self.selected_lig.get(), self.selected_sezon.get())
                # Test
                print("Data extracted!")
                
                self.stop_progress()
                self.update_status("Data extracted successfully!", "green")
                messagebox.showinfo("Success", "Data has been extracted and saved successfully!")
                
                # Close driver
                time.sleep(randomize_sleep_time(2))
                self.driver.quit()
                
                # Reset application
                self.reset_app()
                
            except Exception as e:
                self.stop_progress()
                self.update_status(f"Error: {str(e)}", "red")
                messagebox.showerror("Error", f"Error extracting data: {str(e)}")
                self.data_button.config(state="normal")
        
        threading.Thread(target=run, daemon=True).start()
    
    def reset_app(self):
        # Reset all selections
        self.selected_lig.set("")
        self.selected_sezon.set("")
        
        # Reset combo boxes
        self.lig_combo.config(state="disabled")
        self.lig_combo['values'] = []
        self.sezon_combo.config(state="disabled")
        self.sezon_combo['values'] = []
        
        # Reset buttons
        self.start_button.config(state="normal")
        self.lig_select_button.config(state="disabled")
        self.sezon_select_button.config(state="disabled")
        self.data_button.config(state="disabled")
        
        self.update_status("Ready to start", "green")

if __name__ == "__main__":
    root = tk.Tk()
    app = IddaaFiksturApp(root)
    root.mainloop()