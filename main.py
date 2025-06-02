import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import pandas as pd
import os
import threading
from xml_generator import generate_tally_xml
from tally_sender import send_to_tally

class ExcelToTallyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel to Tally Transfer Tool")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variables
        self.excel_file_path = ""
        self.transactions = []
        self.xml_data = ""
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Excel to Tally Transfer Tool", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Step 1: File selection
        ttk.Label(main_frame, text="Step 1: Select Excel File", 
                 font=('Arial', 12, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Button(file_frame, text="Browse", 
                  command=self.select_file).grid(row=0, column=0, padx=(0, 10))
        
        self.file_label = ttk.Label(file_frame, text="No file selected", 
                                   foreground="gray")
        self.file_label.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Step 2: Preview button
        ttk.Label(main_frame, text="Step 2: Preview Data", 
                 font=('Arial', 12, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=(10, 5))
        
        self.preview_button = ttk.Button(main_frame, text="Load & Preview Data", 
                                        command=self.load_and_preview, state='disabled')
        self.preview_button.grid(row=3, column=1, sticky=tk.W, pady=(10, 5))
        
        # Preview area
        preview_frame = ttk.LabelFrame(main_frame, text="Data Preview", padding="5")
        preview_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        
        self.preview_text = scrolledtext.ScrolledText(preview_frame, height=15, width=80)
        self.preview_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Step 3: Transfer button
        ttk.Label(main_frame, text="Step 3: Transfer to Tally", 
                 font=('Arial', 12, 'bold')).grid(row=5, column=0, sticky=tk.W, pady=(10, 5))
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=10)
        
        self.transfer_button = ttk.Button(button_frame, text="Transfer to Tally", 
                                         command=self.confirm_transfer, state='disabled')
        self.transfer_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready. Please select an Excel file.", 
                                     foreground="blue")
        self.status_label.grid(row=8, column=0, columnspan=3, pady=5)
        
    def select_file(self):
        """Open file dialog to select Excel file"""
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        
        if file_path:
            self.excel_file_path = file_path
            self.file_label.config(text=os.path.basename(file_path), foreground="black")
            self.preview_button.config(state='normal')
            self.status_label.config(text="File selected. Click 'Load & Preview Data'.", 
                                   foreground="blue")
            
            # Clear previous data
            self.transactions = []
            self.transfer_button.config(state='disabled')
            self.preview_text.delete(1.0, tk.END)
    
    def validate_excel_format(self, df):
        """Validate Excel format"""
        required_columns = ['Date', 'Amount', 'Narration', 'GL']
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Remove empty rows
        df = df.dropna(how='all')
        
        if len(df) == 0:
            raise ValueError("No data found in Excel file")
        
        # Basic validation
        for index, row in df.iterrows():
            if pd.isna(row['Date']):
                raise ValueError(f"Row {index + 2}: Date cannot be empty")
            if pd.isna(row['Amount']):
                raise ValueError(f"Row {index + 2}: Amount cannot be empty")
            if pd.isna(row['GL']) or str(row['GL']).strip() == '':
                raise ValueError(f"Row {index + 2}: GL cannot be empty")
        
        return df
    
    def load_and_preview(self):
        """Load Excel data and show preview"""
        try:
            self.status_label.config(text="Loading Excel file...", foreground="blue")
            self.root.update()
            
            # Read Excel file
            df = pd.read_excel(self.excel_file_path)
            df = self.validate_excel_format(df)
            self.transactions = df.to_dict(orient='records')
            
            # Show preview
            preview_text = f"✓ Excel file loaded successfully!\n"
            preview_text += f"✓ Found {len(self.transactions)} valid transactions\n\n"
            preview_text += "="*60 + "\n"
            preview_text += "PREVIEW OF TRANSACTIONS TO BE SENT TO TALLY\n"
            preview_text += "="*60 + "\n\n"
            
            # Show first 5 transactions
            for i, txn in enumerate(self.transactions[:5]):
                preview_text += f"Transaction {i+1}:\n"
                preview_text += f"  Date: {txn['Date']}\n"
                preview_text += f"  Amount: {txn['Amount']}\n"
                preview_text += f"  Narration: {txn['Narration']}\n"
                preview_text += f"  GL Account: {txn['GL']}\n"
                
                # Show accounting logic
                amount = float(txn['Amount'])
                if amount >= 0:
                    preview_text += f"  → Debit: Cash, Credit: {txn['GL']}\n"
                else:
                    preview_text += f"  → Debit: {txn['GL']}, Credit: Cash\n"
                preview_text += "\n"
            
            if len(self.transactions) > 5:
                preview_text += f"... and {len(self.transactions) - 5} more transactions\n\n"
            
            preview_text += "="*60 + "\n"
            preview_text += "Ready to transfer to Tally!\n"
            preview_text += "Click 'Transfer to Tally' to proceed."
            
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(1.0, preview_text)
            
            self.transfer_button.config(state='normal')
            self.status_label.config(text=f"✓ Loaded {len(self.transactions)} transactions. Ready to transfer.", 
                                   foreground="green")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error loading Excel file:\n\n{str(e)}")
            self.status_label.config(text="Error loading file. Please check and try again.", 
                                   foreground="red")
    
    def confirm_transfer(self):
        """Show confirmation dialog before transfer"""
        message = f"Ready to transfer {len(self.transactions)} transactions to Tally.\n\n"
        message += "Before proceeding, please ensure:\n"
        message += "• Tally is running\n"
        message += "• Gateway is enabled in Tally\n"
        message += "• Company is open in Tally\n"
        message += "• All GL accounts exist in Tally\n\n"
        message += "Do you want to proceed?"
        
        if messagebox.askyesno("Confirm Transfer", message):
            self.transfer_to_tally()
    
    def transfer_to_tally(self):
        """Transfer data to Tally in background thread"""
        def transfer_task():
            try:
                self.transfer_button.config(state='disabled')
                self.status_label.config(text="Generating XML...", foreground="blue")
                self.root.update()
                
                # Generate XML
                self.xml_data = generate_tally_xml(self.transactions)
                
                # Save XML preview
                preview_file = "tally_preview.xml"
                with open(preview_file, "w", encoding="utf-8") as f:
                    f.write(self.xml_data)
                
                self.status_label.config(text="Sending to Tally...", foreground="blue")
                self.root.update()
                
                # Send to Tally
                success = send_to_tally(self.xml_data)
                
                
                if success:
                    messagebox.showinfo("Success", 
                                      f"✓ Successfully transferred {len(self.transactions)} transactions to Tally!\n\n"
                                      f"XML preview saved as: {preview_file}")
                    self.status_label.config(text="✓ Transfer completed successfully!", 
                                           foreground="green")
                else:
                    messagebox.showerror("Transfer Failed", 
                                       f"Failed to transfer data to Tally.\n\n"
                                       f"Please check:\n"
                                       f"• Tally is running and Gateway is enabled\n"
                                       f"• All GL accounts exist in Tally\n"
                                       f"• XML preview saved as: {preview_file}")
                    self.status_label.config(text="Transfer failed. Check Tally connection.", 
                                           foreground="red")
                
                self.transfer_button.config(state='normal')
                
            except Exception as e:
                self.transfer_button.config(state='normal')
                messagebox.showerror("Error", f"Unexpected error during transfer:\n\n{str(e)}")
                self.status_label.config(text="Transfer error occurred.", foreground="red")
        
        # Run transfer in background thread
        thread = threading.Thread(target=transfer_task, daemon=True)
        thread.start()

def main():
    root = tk.Tk()
    app = ExcelToTallyGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()