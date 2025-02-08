import random
import customtkinter as ctk
from datetime import datetime
from pathlib import Path
import csv
from tkinter import filedialog
from PIL import Image
import shutil

class DashboardWindow:
    def __init__(self, case_id, master_file, cases_dir):
        self.window = ctk.CTkToplevel()
        self.window.title("Case Dashboard")
        # Remove fullscreen and set a large default size
        self.window.geometry("1200x800")
        # Allow window to be resized
        self.window.resizable(True, True)
        
        # Store case info
        self.case_id = case_id
        self.master_file = master_file
        self.cases_dir = cases_dir
        
        # Create main container
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Header with Case ID
        self.header_label = ctk.CTkLabel(
            self.main_frame, 
            text=f"Case Dashboard - {self.case_id}",
            font=("Arial", 24, "bold")
        )
        self.header_label.pack(pady=20)
        
        # Create grid for dashboard options
        self.options_frame = ctk.CTkFrame(self.main_frame)
        self.options_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create dashboard options
        self.create_dashboard_options()
        
    def create_dashboard_options(self):
        # Define dashboard options
        options = [
            ("👤 Add Suspect", self.add_suspect),
            ("📄 Add Evidence", self.add_evidence),
            ("📝 Case Notes", self.add_notes),
            ("📸 Case Gallery", self.view_gallery),
            ("⏱️ Timeline", self.view_timeline),
            ("📊 Reports", self.generate_reports),
            ("🔍 Search", self.search_case),
            ("📤 Export Case", self.export_case)
        ]
        
        # Create grid layout
        for i, (title, command) in enumerate(options):
            row = i // 3
            col = i % 3
            
            # Create button with appropriate size for windowed mode
            btn = ctk.CTkButton(
                self.options_frame,
                text=title,
                command=command,
                width=250,  # Adjusted width
                height=120,  # Adjusted height
                font=("Arial", 18)  # Adjusted font size
            )
            btn.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")  # Adjusted padding
            
            # Configure grid weights for better spacing
            self.options_frame.grid_columnconfigure(col, weight=1)
            self.options_frame.grid_rowconfigure(row, weight=1)
    
    def add_suspect(self):
        # Create suspect entry window
        suspect_window = ctk.CTkToplevel(self.window)
        suspect_window.title("Add Suspect")
        suspect_window.geometry("500x800")  # Increased height for image section
        
        # Add your suspect form here
        frame = ctk.CTkFrame(suspect_window)
        frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Title
        ctk.CTkLabel(frame, text="Add Suspect Details", font=("Arial", 18, "bold")).pack(pady=10)
        
        # Image Upload Section
        image_frame = ctk.CTkFrame(frame)
        image_frame.pack(fill="x", padx=10, pady=10)
        
        # Variable to store the image path
        selected_image_path = ctk.StringVar()
        
        def upload_image():
            file_path = filedialog.askopenfilename(
                title="Select Suspect Image",
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
            )
            if file_path:
                selected_image_path.set(file_path)
                image_label.configure(text=f"Selected: {file_path.split('/')[-1]}")
        
        # Image upload button and label
        ctk.CTkButton(
            image_frame, 
            text="Upload Suspect Image", 
            command=upload_image
        ).pack(side="left", padx=10)
        
        image_label = ctk.CTkLabel(image_frame, text="No image selected")
        image_label.pack(side="left", padx=10)
        
        # Create entry fields
        fields = [
            ("Name:", "name"),
            ("Age:", "age"),
            ("Gender:", "gender"),
            ("Height:", "height"),
            ("Weight:", "weight"),
            ("Identifying Marks:", "marks"),
            ("Last Known Address:", "address"),
            ("Contact Information:", "contact")
        ]
        
        entries = {}
        for label_text, key in fields:
            field_frame = ctk.CTkFrame(frame)
            field_frame.pack(fill="x", padx=10, pady=5)
            ctk.CTkLabel(field_frame, text=label_text).pack(side="left", padx=10)
            entry = ctk.CTkEntry(field_frame, width=300)
            entry.pack(side="left", padx=10)
            entries[key] = entry
        
        # Additional Notes Text Box
        ctk.CTkLabel(frame, text="Additional Notes:").pack(anchor="w", padx=20, pady=(10,0))
        notes_text = ctk.CTkTextbox(frame, height=100)
        notes_text.pack(padx=20, pady=(5,10), fill="x")
        
        def save_suspect():
            try:
                # Create case folder if it doesn't exist
                case_folder = self.cases_dir / self.case_id
                case_folder.mkdir(exist_ok=True)
                
                # Handle image saving
                image_filename = ""
                if selected_image_path.get():
                    # Create images folder if it doesn't exist
                    images_folder = case_folder / "images"
                    images_folder.mkdir(exist_ok=True)
                    
                    # Create unique filename using suspect name
                    suspect_name = entries['name'].get() or datetime.now().strftime('%Y%m%d_%H%M%S')
                    image_ext = selected_image_path.get().split('.')[-1]
                    image_filename = f"{suspect_name}.{image_ext}"
                    
                    # Copy image to images folder
                    image_destination = images_folder / image_filename
                    shutil.copy2(selected_image_path.get(), image_destination)
                
                # Prepare suspect data
                suspect_data = {
                    'Suspect Name': entries['name'].get(),
                    'Age': entries['age'].get(),
                    'Gender': entries['gender'].get(),
                    'Height': entries['height'].get(),
                    'Weight': entries['weight'].get(),
                    'Identifying Marks': entries['marks'].get(),
                    'Address': entries['address'].get(),
                    'Contact': entries['contact'].get(),
                    'Notes': notes_text.get("1.0", "end-1c"),
                    'Image': image_filename,
                    'Date Added': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                # Save to CSV file
                suspects_file = case_folder / f"{self.case_id}_suspects.csv"
                is_new_file = not suspects_file.exists()
                
                with open(suspects_file, 'a', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=list(suspect_data.keys()))
                    if is_new_file:
                        writer.writeheader()
                    writer.writerow(suspect_data)
                
                self.show_message("Success", "Suspect details have been saved successfully!")
                suspect_window.destroy()
                
            except Exception as e:
                self.show_message("Error", f"An error occurred: {str(e)}")
        
        # Save Button
        ctk.CTkButton(frame, text="Save Suspect Details", command=save_suspect).pack(pady=20)
    
    def add_evidence(self):
        # Create evidence entry window
        evidence_window = ctk.CTkToplevel(self.window)
        evidence_window.title("Add Evidence")
        evidence_window.geometry("500x800")
        
        # Add evidence form
        frame = ctk.CTkFrame(evidence_window)
        frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Title
        ctk.CTkLabel(frame, text="Add Evidence Details", font=("Arial", 18, "bold")).pack(pady=10)
        
        # Images Upload Section
        image_frame = ctk.CTkFrame(frame)
        image_frame.pack(fill="x", padx=10, pady=10)
        
        # List to store selected image paths
        selected_images = []
        
        # Label to show selected image count
        image_count_label = ctk.CTkLabel(image_frame, text="No images selected")
        
        def upload_images():
            file_paths = filedialog.askopenfilenames(
                title="Select Evidence Images",
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
            )
            if file_paths:
                selected_images.extend(file_paths)
                image_count_label.configure(text=f"Selected: {len(selected_images)} images")
        
        def clear_images():
            selected_images.clear()
            image_count_label.configure(text="No images selected")
        
        # Image upload buttons and label
        ctk.CTkButton(
            image_frame, 
            text="Upload Images", 
            command=upload_images
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            image_frame, 
            text="Clear Images", 
            command=clear_images
        ).pack(side="left", padx=10)
        
        image_count_label.pack(side="left", padx=10)
        
        # Create entry fields
        fields = [
            ("Evidence ID:", "id"),
            ("Evidence Type:", "type"),
            ("Location Found:", "location"),
            ("Date Found:", "date_found"),
            ("Found By:", "found_by"),
            ("Condition:", "condition"),
            ("Storage Location:", "storage_location")
        ]
        
        entries = {}
        for label_text, key in fields:
            field_frame = ctk.CTkFrame(frame)
            field_frame.pack(fill="x", padx=10, pady=5)
            ctk.CTkLabel(field_frame, text=label_text).pack(side="left", padx=10)
            entry = ctk.CTkEntry(field_frame, width=300)
            entry.pack(side="left", padx=10)
            entries[key] = entry
        
        # Description Text Box
        ctk.CTkLabel(frame, text="Evidence Description:").pack(anchor="w", padx=20, pady=(10,0))
        description_text = ctk.CTkTextbox(frame, height=100)
        description_text.pack(padx=20, pady=(5,10), fill="x")
        
        def save_evidence():
            try:
                # Create case folder if it doesn't exist
                case_folder = self.cases_dir / self.case_id
                case_folder.mkdir(exist_ok=True)
                
                # Create evidence folder
                evidence_folder = case_folder / "evidence"
                evidence_folder.mkdir(exist_ok=True)
                
                # Create unique evidence ID if not provided
                evidence_id = entries['id'].get() or f"EVD{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                # Handle multiple images
                image_filenames = []
                if selected_images:
                    # Create images folder for this evidence
                    images_folder = evidence_folder / evidence_id / "images"
                    images_folder.mkdir(parents=True, exist_ok=True)
                    
                    # Copy all selected images
                    for i, image_path in enumerate(selected_images):
                        image_ext = image_path.split('.')[-1]
                        image_filename = f"{evidence_id}_img{i+1}.{image_ext}"
                        image_destination = images_folder / image_filename
                        shutil.copy2(image_path, image_destination)
                        image_filenames.append(image_filename)
                
                # Prepare evidence data
                evidence_data = {
                    'Evidence ID': evidence_id,
                    'Type': entries['type'].get(),
                    'Location Found': entries['location'].get(),
                    'Date Found': entries['date_found'].get(),
                    'Found By': entries['found_by'].get(),
                    'Condition': entries['condition'].get(),
                    'Storage Location': entries['storage_location'].get(),
                    'Description': description_text.get("1.0", "end-1c"),
                    'Images': ', '.join(image_filenames),
                    'Date Added': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                # Save to CSV file
                evidence_file = case_folder / f"{self.case_id}_evidence.csv"
                is_new_file = not evidence_file.exists()
                
                with open(evidence_file, 'a', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=list(evidence_data.keys()))
                    if is_new_file:
                        writer.writeheader()
                    writer.writerow(evidence_data)
                
                self.show_message("Success", "Evidence details have been saved successfully!")
                evidence_window.destroy()
                
            except Exception as e:
                self.show_message("Error", f"An error occurred: {str(e)}")
        
        # Save Button
        ctk.CTkButton(frame, text="Save Evidence Details", command=save_evidence).pack(pady=20)
    
    def add_notes(self):
        self.show_message("Coming Soon", "Notes addition feature will be available soon!")
        
    def view_gallery(self):
        self.show_message("Coming Soon", "Gallery feature will be available soon!")
        
    def view_timeline(self):
        self.show_message("Coming Soon", "Timeline feature will be available soon!")
        
    def generate_reports(self):
        self.show_message("Coming Soon", "Reports feature will be available soon!")
        
    def search_case(self):
        self.show_message("Coming Soon", "Search feature will be available soon!")
        
    def export_case(self):
        self.show_message("Coming Soon", "Export feature will be available soon!")
    
    def show_message(self, title, message):
        message_window = ctk.CTkToplevel(self.window)
        message_window.title(title)
        message_window.geometry("300x150")
        message_window.transient(self.window)
        message_window.grab_set()
        
        ctk.CTkLabel(message_window, text=message, wraplength=250).pack(pady=20)
        ctk.CTkButton(message_window, text="OK", command=message_window.destroy).pack()

class InvestigationApp:
    def __init__(self):
        # Configure appearance and window
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Create base directories if they don't exist
        self.cases_dir = Path("cases")
        self.cases_dir.mkdir(exist_ok=True)
        
        # Create or check for master CSV file
        self.master_file = self.cases_dir / "cases_master.csv"
        if not self.master_file.exists():
            with open(self.master_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Case ID', 'Date Created', 'Investigator Name', 'Contact Info', 'Case Title', 'Description'])
        
        self.window = ctk.CTk()
        self.window.title("Crime Investigation System")
        self.window.geometry("600x400")
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Crime Investigation System", 
            font=("Arial", 24, "bold")
        )
        self.title_label.pack(pady=30)
        
        # Buttons Frame
        self.buttons_frame = ctk.CTkFrame(self.main_frame)
        self.buttons_frame.pack(pady=20)
        
        # New Case Button
        self.new_case_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Create New Case",
            command=self.create_new_case,
            width=200,
            height=50,
            font=("Arial", 16)
        )
        self.new_case_btn.pack(pady=20)
        
        # Reopen Case Button
        self.reopen_case_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Reopen Existing Case",
            command=self.reopen_case,
            width=200,
            height=50,
            font=("Arial", 16)
        )
        self.reopen_case_btn.pack(pady=20)
        
        # Initialize case entry form as None
        self.case_entry_frame = None
    
    def create_new_case(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Create case entry form
        self.create_case_entry_form()
    
    def reopen_case(self):
        # Create case selection window
        reopen_window = ctk.CTkToplevel(self.window)
        reopen_window.title("Reopen Case")
        reopen_window.geometry("800x600")
        
        # Create main frame
        frame = ctk.CTkFrame(reopen_window)
        frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Title
        ctk.CTkLabel(frame, text="Select Case to Reopen", font=("Arial", 20, "bold")).pack(pady=10)
        
        # Create scrollable frame for cases
        cases_frame = ctk.CTkScrollableFrame(frame)
        cases_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        try:
            with open(self.master_file, 'r', newline='') as f:
                reader = csv.reader(f)
                headers = next(reader)  # Skip header row
                
                for row in reader:
                    case_id, date_created, investigator, _, title, _ = row
                    case_frame = ctk.CTkFrame(cases_frame)
                    case_frame.pack(fill="x", padx=5, pady=5)
                    
                    case_info = f"Case ID: {case_id}\nDate: {date_created}\nInvestigator: {investigator}\nTitle: {title}"
                    ctk.CTkLabel(case_frame, text=case_info, justify="left").pack(side="left", padx=10)
                    
                    def open_case(cid=case_id):
                        dashboard = DashboardWindow(cid, str(self.master_file), self.cases_dir)
                        reopen_window.destroy()
                    
                    ctk.CTkButton(
                        case_frame,
                        text="Open Case",
                        command=open_case,
                        width=100
                    ).pack(side="right", padx=10)
        
        except Exception as e:
            ctk.CTkLabel(cases_frame, text=f"Error loading cases: {str(e)}").pack(pady=20)
    
    def create_case_entry_form(self):
        # Title
        self.title_label = ctk.CTkLabel(self.main_frame, text="New Case Entry", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=10)
        
        # Generate Case ID
        self.case_id = f"CASE{datetime.now().strftime('%Y%m%d')}{random.randint(1000,9999)}"
        self.case_id_frame = ctk.CTkFrame(self.main_frame)
        self.case_id_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(self.case_id_frame, text="Case ID:").pack(side="left")
        self.case_id_label = ctk.CTkLabel(self.case_id_frame, text=self.case_id)
        self.case_id_label.pack(side="left", padx=10)
        
        # Investigator Name
        self.name_entry = self.create_entry_field("Investigator Name:")
        
        # Contact Information
        self.contact_entry = self.create_entry_field("Contact Information:")
        
        # Case Title
        self.case_title_entry = self.create_entry_field("Case Title:")
        
        # Description
        ctk.CTkLabel(self.main_frame, text="Case Description:").pack(anchor="w", padx=20, pady=(10,0))
        self.description_text = ctk.CTkTextbox(self.main_frame, height=150)
        self.description_text.pack(padx=20, pady=(5,10), fill="x")
        
        # Submit Button
        self.submit_button = ctk.CTkButton(self.main_frame, text="Submit Case", command=self.submit_case)
        self.submit_button.pack(pady=20)
    
    def create_entry_field(self, label_text):
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(frame, text=label_text).pack(side="left")
        entry = ctk.CTkEntry(frame, width=400)
        entry.pack(side="left", padx=10)
        return entry
    
    def submit_case(self):
        # Get all the case details
        case_data = {
            'Case ID': self.case_id,
            'Date Created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Investigator Name': self.name_entry.get(),
            'Contact Info': self.contact_entry.get(),
            'Case Title': self.case_title_entry.get(),
            'Description': self.description_text.get("1.0", "end-1c")
        }
        
        try:
            # Create case folder
            case_folder = self.cases_dir / self.case_id
            case_folder.mkdir(exist_ok=True)
            
            # Save case details to individual file
            case_details_file = case_folder / "case_details.txt"
            with open(case_details_file, 'w') as f:
                for key, value in case_data.items():
                    f.write(f"{key}: {value}\n")
            
            # Append to master CSV
            with open(self.master_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(case_data.values())
            
            # Open dashboard with cases_dir
            dashboard = DashboardWindow(self.case_id, str(self.master_file), self.cases_dir)
            
            # Clear the form
            self.clear_form()
            
        except Exception as e:
            self.show_message("Error", f"An error occurred: {str(e)}")
    
    def show_message(self, title, message):
        message_window = ctk.CTkToplevel(self.window)
        message_window.title(title)
        message_window.geometry("300x150")
        
        # Center the message window
        message_window.transient(self.window)
        message_window.grab_set()
        
        ctk.CTkLabel(message_window, text=message, wraplength=250).pack(pady=20)
        ctk.CTkButton(message_window, text="OK", command=message_window.destroy).pack()
    
    def clear_form(self):
        # Generate new case ID
        self.case_id = f"CASE{datetime.now().strftime('%Y%m%d')}{random.randint(1000,9999)}"
        self.case_id_label.configure(text=self.case_id)
        
        # Clear all fields
        self.name_entry.delete(0, 'end')
        self.contact_entry.delete(0, 'end')
        self.case_title_entry.delete(0, 'end')
        self.description_text.delete("1.0", "end")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = InvestigationApp()
    app.run()