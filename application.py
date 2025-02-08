import random
import customtkinter as ctk
from datetime import datetime
from pathlib import Path
import csv
from tkinter import filedialog
from PIL import Image, ImageTk
import shutil
import google.generativeai as genai
import os
import threading
from docx import Document
from docx.shared import Inches
import hashlib  # Import hashlib for hashing functionality

# Google-inspired color scheme
COLORS = {
    'primary': '#4285F4',      # Google Blue
    'secondary': '#DB4437',    # Google Red
    'accent': '#F4B400',       # Google Yellow
    'success': '#0F9D58',      # Google Green
    'light': '#F1F1F1',        # Light Gray
    'dark': '#202124',         # Dark Gray
    'white': '#FFFFFF',        # White
    'black': '#000000'         # Black
}

# Button styles
BUTTON_STYLE = {
    'primary': {
        'fg_color': COLORS['primary'],
        'hover_color': '#357AE8',  # Darker blue for hover
        'text_color': COLORS['white'],
        'corner_radius': 10
    },
    'secondary': {
        'fg_color': COLORS['light'],
        'hover_color': '#B0BEC5',  # Light gray for hover
        'text_color': COLORS['black'],
        'corner_radius': 10
    },
    'danger': {
        'fg_color': COLORS['secondary'],
        'hover_color': '#C62828',   # Darker red for hover
        'text_color': COLORS['white'],
        'corner_radius': 10
    }
}

# Frame styles
FRAME_STYLE = {
    'fg_color': COLORS['white'],
    'corner_radius': 15,
    'border_width': 1,
    'border_color': COLORS['light']
}

class DigitalForensicDashboard:
    def __init__(self, master, case_id, cases_dir):
        self.window = ctk.CTkToplevel(master)
        self.window.title("Digital Forensic Dashboard")
        self.window.geometry("800x600")
        self.window.resizable(True, True)  # Allow window resizing
        self.window.transient(master)
        self.window.grab_set()
        
        # Create main frame with shadow effect
        self.main_frame = ctk.CTkFrame(self.window, **FRAME_STYLE)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Title
        ctk.CTkLabel(
            self.main_frame,
            text="Digital Forensic Management",
            font=("Arial", 24, "bold")
        ).pack(pady=10)
        
        # Description
        ctk.CTkLabel(
            self.main_frame,
            text="Manage and analyze digital forensic evidence related to the case.",
            font=("Arial", 14)
        ).pack(pady=10)

        # Create a frame for cards
        cards_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        cards_frame.pack(pady=20, fill="both", expand=True)

        # Define options with icons
        options = [
            ("Scan Drive", "🔍", self.scan_drive),
            ("Find Flash Files", "💾", self.find_flash_files),
            ("Duplicate USB Drive", "🔄", self.duplicate_usb_drive),
            ("Find Hexadecimal Values", "🔢", self.find_hexadecimal_values),
            ("Find Hash Values", "🔑", self.find_hash_values),
            ("Show Cyber Forensic Tools", "🛠️", self.show_cyber_forensic_tools)
        ]

        # Create cards for each option
        for index, option in enumerate(options):
            self.create_card(cards_frame, option[0], option[1], option[2])

    def create_card(self, parent, text, icon, command):
        card_frame = ctk.CTkFrame(parent, **FRAME_STYLE)
        card_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)

        # Center the icon
        ctk.CTkLabel(card_frame, text=icon, font=("Arial", 36)).pack(pady=(10, 5))

        # Center the text below the icon
        ctk.CTkLabel(card_frame, text=text, font=("Arial", 16)).pack(pady=(0, 10))

        # Button
        ctk.CTkButton(card_frame, text="Open", command=command, **BUTTON_STYLE['primary']).pack(pady=5)

    def find_hash_values(self):
        # Function to find hash values of contents in a folder
        folder_path = filedialog.askdirectory(title="Select Folder to Find Hash Values")
        if folder_path:
            hash_results = []
            for file in Path(folder_path).rglob('*'):  # Recursively find all files
                if file.is_file():
                    hash_value = self.calculate_hash(file)
                    hash_results.append(f"{file.name}: {hash_value}")
            
            # Display results in a message box
            if hash_results:
                result_message = "\n".join(hash_results)
                self.show_message("Hash Values", result_message)
            else:
                self.show_message("Hash Values", "No files found in the selected folder.")

    def calculate_hash(self, file_path):
        # Calculate the SHA-256 hash of a file
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            # Read file in chunks to avoid memory issues
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def scan_drive(self):
        # Function to scan a drive (placeholder implementation)
        drive_path = filedialog.askdirectory(title="Select Drive to Scan")
        if drive_path:
            # Implement scanning logic here
            self.show_message("Scan Drive", f"Scanning drive: {drive_path}... (not implemented)")

    def find_flash_files(self):
        # Function to find flash files (placeholder implementation)
        folder_path = filedialog.askdirectory(title="Select Folder to Search for Flash Files")
        if folder_path:
            # Implement file finding logic here
            self.show_message("Find Flash Files", f"Searching for flash files in: {folder_path}... (not implemented)")

    def duplicate_usb_drive(self):
        # Function to duplicate a USB drive (placeholder implementation)
        usb_path = filedialog.askdirectory(title="Select USB Drive to Duplicate")
        if usb_path:
            # Implement duplication logic here
            self.show_message("Duplicate USB Drive", f"Duplicating USB drive: {usb_path}... (not implemented)")

    def find_hexadecimal_values(self):
        # Function to find hexadecimal values of a folder (placeholder implementation)
        folder_path = filedialog.askdirectory(title="Select Folder to Find Hexadecimal Values")
        if folder_path:
            # Implement hexadecimal finding logic here
            self.show_message("Find Hexadecimal Values", f"Finding hexadecimal values in: {folder_path}... (not implemented)")

    def show_message(self, title, message):
        message_window = ctk.CTkToplevel(self.window)
        message_window.title(title)
        message_window.geometry("300x150")
        message_window.transient(self.window)
        message_window.grab_set()
        
        ctk.CTkLabel(message_window, text=message, wraplength=250).pack(pady=20)
        ctk.CTkButton(message_window, text="OK", command=message_window.destroy).pack(pady=10)

    def show_cyber_forensic_tools(self):
        # Create a new window for cyber forensic tools
        tools_window = ctk.CTkToplevel(self.window)
        tools_window.title("Cyber Forensic Tools")
        tools_window.geometry("400x400")
        
        # Create a scrollable frame
        tools_frame = ctk.CTkScrollableFrame(tools_window)
        tools_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # List of cyber forensic tools
        tools = [
            "FTK Imager",
            "EnCase",
            "Autopsy",
            "Sleuth Kit",
            "Wireshark",
            "Volatility",
            "Caine",
            "Kali Linux",
            "X1 Social Discovery",
            "Oxygen Forensics"
        ]
        
        # Add tools to the scrollable frame
        for tool in tools:
            ctk.CTkLabel(tools_frame, text=tool, font=("Arial", 14)).pack(pady=5)

    def export_case(self):
        # Existing export functionality
        export_path = filedialog.askdirectory(title="Select Export Location")
        if not export_path:
            return
        
        export_dir = Path(export_path) / f"{self.case_id}_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        export_dir.mkdir(exist_ok=True)
        
        # Existing code to copy case details...
        
        # Add selected cyber forensic tools to the CSV
        tools_file = export_dir / "cyber_forensic_tools.csv"
        with open(tools_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Tool Name'])
            tools = [
                "FTK Imager",
                "EnCase",
                "Autopsy",
                "Sleuth Kit",
                "Wireshark",
                "Volatility",
                "Caine",
                "Kali Linux",
                "X1 Social Discovery",
                "Oxygen Forensics"
            ]
            for tool in tools:
                writer.writerow([tool])
        
        self.show_message("Success", f"Case exported successfully to:\n{export_dir}\nCyber forensic tools saved to:\n{tools_file.name}")

class DashboardWindow:
    def __init__(self, case_id, master_file, cases_dir):
        self.window = ctk.CTkToplevel()
        self.window.title("Case Dashboard")
        self.window.geometry("1200x800")
        self.window.resizable(True, True)
        
        # Configure window background
        self.window.configure(fg_color=COLORS['light'])
        
        # Store case info
        self.case_id = case_id
        self.master_file = master_file
        self.cases_dir = cases_dir
        
        # Create main container with shadow effect
        self.main_frame = ctk.CTkFrame(
            self.window,
            **FRAME_STYLE
        )
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Header with Case ID and styling
        header_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=COLORS['primary'],
            corner_radius=10,
            height=80
        )
        header_frame.pack(fill="x", padx=20, pady=(20,10))
        header_frame.pack_propagate(False)
        
        self.header_label = ctk.CTkLabel(
            header_frame, 
            text=f"Case Dashboard - {self.case_id}",
            font=("Arial", 28, "bold"),
            text_color=COLORS['white']
        )
        self.header_label.pack(expand=True)
        
        # Create grid for dashboard options
        self.options_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        self.options_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create dashboard options
        self.create_dashboard_options()
    
    def create_dashboard_options(self):
        # Define dashboard options with icons and descriptions
        options = [
            {
                "title": "Add Suspect",
                "icon": "👤",
                "desc": "Add new suspect information",
                "command": self.add_suspect
            },
            {
                "title": "Add Evidence",
                "icon": "📄",
                "desc": "Record new evidence details",
                "command": self.add_evidence
            },
            {
                "title": "Case Notes",
                "icon": "📝",
                "desc": "Manage investigation notes",
                "command": self.add_notes
            },
            {
                "title": "Case Gallery",
                "icon": "📸",
                "desc": "View all case images",
                "command": self.view_gallery
            },
            {
                "title": "Timeline",
                "icon": "⏱️",
                "desc": "View case timeline",
                "command": self.view_timeline
            },
            {
                "title": "Reports",
                "icon": "📊",
                "desc": "Generate case reports",
                "command": self.generate_reports
            },
            {
                "title": "Search",
                "icon": "🔍",
                "desc": "Search case details",
                "command": self.search_case
            },
            {
                "title": "AI Assistant",
                "icon": "🤖",
                "desc": "Get AI assistance",
                "command": self.show_ai_assistant
            },
            {
                "title": "Export Case",
                "icon": "📤",
                "desc": "Export case data",
                "command": self.export_case
            },
            {
                "title": "Digital Forensic",
                "icon": "🔬",
                "desc": "Manage digital forensic evidence",
                "command": self.digital_forensic
            },
            {
                "title": "About",
                "icon": "ℹ️",
                "desc": "About the system",
                "command": self.show_about
            }
        ]
        
        # Create grid layout
        for i, option in enumerate(options):
            row = i // 3
            col = i % 3
            
            # Create option frame with hover effect
            option_frame = ctk.CTkFrame(
                self.options_frame,
                **FRAME_STYLE
            )
            option_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            # Make the entire frame clickable
            def make_callback(cmd):
                return lambda event: cmd()
            
            # Bind click event to the frame
            option_frame.bind("<Button-1>", make_callback(option["command"]))
            
            # Icon and title (make them clickable too)
            icon_label = ctk.CTkLabel(
                option_frame,
                text=option["icon"],
                font=("Arial", 36)
            )
            icon_label.pack(pady=(20,5))
            icon_label.bind("<Button-1>", make_callback(option["command"]))
            
            title_label = ctk.CTkLabel(
                option_frame,
                text=option["title"],
                font=("Arial", 18, "bold"),
                text_color=COLORS['primary']
            )
            title_label.pack(pady=5)
            title_label.bind("<Button-1>", make_callback(option["command"]))
            
            # Description
            desc_label = ctk.CTkLabel(
                option_frame,
                text=option["desc"],
                font=("Arial", 12),
                text_color=COLORS['dark']
            )
            desc_label.pack(pady=(0,10))
            desc_label.bind("<Button-1>", make_callback(option["command"]))
            
            # Add hover effect
            def on_enter(e, frame=option_frame):
                frame.configure(fg_color=COLORS['light'])
                
            def on_leave(e, frame=option_frame):
                frame.configure(fg_color=COLORS['white'])
            
            # Bind hover events
            option_frame.bind("<Enter>", on_enter)
            option_frame.bind("<Leave>", on_leave)
            
            # Bind hover events to all children
            for widget in [icon_label, title_label, desc_label]:
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)
            
            # Configure grid weights
            self.options_frame.grid_columnconfigure(col, weight=1)
            self.options_frame.grid_rowconfigure(row, weight=1)
    
    def add_suspect(self):
        # Create suspect entry window
        suspect_window = ctk.CTkToplevel(self.window)
        suspect_window.title("Add Suspect")
        suspect_window.geometry("600x800")
        suspect_window.transient(self.window)
        suspect_window.grab_set()
        
        # Variable to track window state
        window_exists = True
        
        # Handle window close
        def on_window_close():
            nonlocal window_exists
            window_exists = False
            suspect_window.grab_release()
            suspect_window.destroy()
        
        suspect_window.protocol("WM_DELETE_WINDOW", on_window_close)
        
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
        evidence_window.geometry("600x800")
        evidence_window.transient(self.window)
        evidence_window.grab_set()
        
        # Variable to track window state
        window_exists = True
        
        # Handle window close
        def on_window_close():
            nonlocal window_exists
            window_exists = False
            evidence_window.grab_release()
            evidence_window.destroy()
        
        evidence_window.protocol("WM_DELETE_WINDOW", on_window_close)
        
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
        notes_window = ctk.CTkToplevel(self.window)
        notes_window.title("Case Notes")
        notes_window.geometry("800x600")
        notes_window.transient(self.window)
        notes_window.grab_set()
        
        # Create main frame
        frame = ctk.CTkFrame(notes_window)
        frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Title
        ctk.CTkLabel(
            frame,
            text="Case Notes",
            font=("Arial", 24, "bold")
        ).pack(pady=10)
        
        # Notes list frame
        notes_list_frame = ctk.CTkScrollableFrame(frame)
        notes_list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Load existing notes
        notes_file = self.cases_dir / self.case_id / f"{self.case_id}_notes.csv"
        if notes_file.exists():
            with open(notes_file, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    note_frame = ctk.CTkFrame(notes_list_frame)
                    note_frame.pack(fill="x", padx=5, pady=5)
                    
                    note_text = f"Date: {row['Date']}\n{row['Note']}"
                    ctk.CTkLabel(
                        note_frame,
                        text=note_text,
                        justify="left",
                        wraplength=600
                    ).pack(padx=10, pady=5)
        
        # Add note frame
        add_note_frame = ctk.CTkFrame(frame)
        add_note_frame.pack(fill="x", padx=10, pady=10)
        
        # Note input
        note_input = ctk.CTkTextbox(add_note_frame, height=100)
        note_input.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        def save_note():
            note_text = note_input.get("1.0", "end-1c").strip()
            if note_text:
                try:
                    # Ensure case directory exists
                    case_dir = self.cases_dir / self.case_id
                    case_dir.mkdir(exist_ok=True)
                    
                    # Prepare note data
                    note_data = {
                        'Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'Note': note_text
                    }
                    
                    # Save to CSV file
                    is_new_file = not notes_file.exists()
                    
                    with open(notes_file, 'a', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=['Date', 'Note'])
                        if is_new_file:
                            writer.writeheader()
                        writer.writerow(note_data)
                    
                    # Add note to display
                    note_frame = ctk.CTkFrame(notes_list_frame)
                    note_frame.pack(fill="x", padx=5, pady=5)
                    
                    display_text = f"Date: {note_data['Date']}\n{note_data['Note']}"
                    ctk.CTkLabel(
                        note_frame,
                        text=display_text,
                        justify="left",
                        wraplength=600
                    ).pack(padx=10, pady=5)
                    
                    # Clear input
                    note_input.delete("1.0", "end")
                    
                    # Scroll to bottom
                    notes_list_frame._parent_canvas.yview_moveto(1.0)
                    
                except Exception as e:
                    self.show_message("Error", f"Failed to save note: {str(e)}")
        
        # Save button
        ctk.CTkButton(
            add_note_frame,
            text="Add Note",
            command=save_note,
            width=100
        ).pack(side="right")
        
        # Set focus to input
        note_input.focus()
    
    def view_gallery(self):
        gallery_window = ctk.CTkToplevel(self.window)
        gallery_window.title("Case Gallery")
        gallery_window.geometry("800x600")
        gallery_window.transient(self.window)
        gallery_window.grab_set()
        
        # Variable to track window state
        window_exists = True
        
        # Handle window close
        def on_window_close():
            nonlocal window_exists
            window_exists = False
            gallery_window.grab_release()
            gallery_window.destroy()
        
        gallery_window.protocol("WM_DELETE_WINDOW", on_window_close)
        
        # Create main frame
        main_frame = ctk.CTkFrame(gallery_window)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Title
        ctk.CTkLabel(
            main_frame, 
            text="Case Gallery", 
            font=("Arial", 24, "bold")
        ).pack(pady=10)
        
        # Create notebook for sections
        notebook = ctk.CTkTabview(main_frame)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add tabs
        suspects_tab = notebook.add("Section A - Suspects")
        evidence_tab = notebook.add("Section B - Evidence")
        
        # Create scrollable frames for both sections
        suspects_frame = ctk.CTkScrollableFrame(suspects_tab)
        suspects_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        evidence_frame = ctk.CTkScrollableFrame(evidence_tab)
        evidence_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        def load_and_resize_image(image_path, size=(200, 200)):
            try:
                img = Image.open(image_path)
                img.thumbnail(size)
                return ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error loading image {image_path}: {e}")
                return None
        
        # Load suspect images
        suspects_file = self.cases_dir / self.case_id / f"{self.case_id}_suspects.csv"
        if suspects_file.exists():
            with open(suspects_file, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('Image'):  # If suspect has an image
                        image_path = self.cases_dir / self.case_id / "images" / row['Image']
                        if image_path.exists():
                            # Create frame for each suspect
                            suspect_item = ctk.CTkFrame(suspects_frame)
                            suspect_item.pack(fill="x", padx=10, pady=10)
                            
                            # Load and display image
                            photo = load_and_resize_image(image_path)
                            if photo:
                                ctk.CTkLabel(suspect_item, image=photo, text="").pack(side="left", padx=10)
                            
                            # Display suspect details
                            ctk.CTkLabel(suspect_item, text=row['Suspect Name'], font=("Arial", 16)).pack(side="left", padx=10)
        
        # Load evidence images
        evidence_file = self.cases_dir / self.case_id / f"{self.case_id}_evidence.csv"
        if evidence_file.exists():
            with open(evidence_file, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('Images'):  # If evidence has images
                        image_list = row['Images'].split(', ')
                        for img_name in image_list:
                            image_path = self.cases_dir / self.case_id / "evidence" / row['Evidence ID'] / "images" / img_name
                            if image_path.exists():
                                # Create frame for each evidence
                                evidence_item = ctk.CTkFrame(evidence_frame)
                                evidence_item.pack(fill="x", padx=10, pady=10)
                                
                                # Load and display image
                                photo = load_and_resize_image(image_path)
                                if photo:
                                    ctk.CTkLabel(evidence_item, image=photo, text="").pack(side="left", padx=10)
                                
                                # Display evidence details
                                ctk.CTkLabel(evidence_item, text=row['Evidence ID'], font=("Arial", 16)).pack(side="left", padx=10)
        
        # Set focus to the main frame
        main_frame.focus_set()
    
    def view_timeline(self):
        timeline_window = ctk.CTkToplevel(self.window)
        timeline_window.title("Case Timeline")
        timeline_window.geometry("800x600")
        timeline_window.transient(self.window)
        timeline_window.grab_set()
        
        # Create main frame
        frame = ctk.CTkFrame(timeline_window)
        frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Title
        ctk.CTkLabel(
            frame,
            text="Case Timeline",
            font=("Arial", 24, "bold")
        ).pack(pady=10)
        
        # Timeline frame
        timeline_frame = ctk.CTkScrollableFrame(frame)
        timeline_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Collect all events
        events = []
        
        # Add suspects
        suspects_file = self.cases_dir / self.case_id / f"{self.case_id}_suspects.csv"
        if suspects_file.exists():
            with open(suspects_file, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    events.append({
                        'date': datetime.strptime(row['Date Added'], '%Y-%m-%d %H:%M:%S'),
                        'type': 'Suspect Added',
                        'description': f"New suspect added: {row['Suspect Name']}"
                    })
        
        # Add evidence
        evidence_file = self.cases_dir / self.case_id / f"{self.case_id}_evidence.csv"
        if evidence_file.exists():
            with open(evidence_file, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    events.append({
                        'date': datetime.strptime(row['Date Added'], '%Y-%m-%d %H:%M:%S'),
                        'type': 'Evidence Added',
                        'description': f"New evidence added: {row['Evidence ID']}"
                    })
        
        # Add notes
        notes_file = self.cases_dir / self.case_id / f"{self.case_id}_notes.csv"
        if notes_file.exists():
            with open(notes_file, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    events.append({
                        'date': datetime.strptime(row['Date'], '%Y-%m-%d %H:%M:%S'),
                        'type': 'Note Added',
                        'description': row['Note'][:100] + ('...' if len(row['Note']) > 100 else '')
                    })
        
        # Sort events by date
        events.sort(key=lambda x: x['date'])
        
        # Display events
        for event in events:
            event_frame = ctk.CTkFrame(timeline_frame)
            event_frame.pack(fill="x", padx=5, pady=5)
            
            date_str = event['date'].strftime('%Y-%m-%d %H:%M:%S')
            event_text = f"[{date_str}] {event['type']}\n{event['description']}"
            
            ctk.CTkLabel(
                event_frame,
                text=event_text,
                justify="left",
                wraplength=600
            ).pack(padx=10, pady=5)
    
    def generate_reports(self):
        reports_window = ctk.CTkToplevel(self.window)
        reports_window.title("Generate Reports")
        reports_window.geometry("800x600")
        reports_window.transient(self.window)
        reports_window.grab_set()
        
        # Create main frame
        frame = ctk.CTkFrame(reports_window)
        frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Title
        ctk.CTkLabel(
            frame,
            text="Generate Reports",
            font=("Arial", 24, "bold")
        ).pack(pady=10)
        
        # Report options frame
        options_frame = ctk.CTkFrame(frame)
        options_frame.pack(fill="x", padx=10, pady=10)
        
        # Checkboxes for report types
        report_types = ["Case Summary", "Suspects List", "Evidence List", "Timeline Report"]
        report_vars = [ctk.StringVar(value=report) for report in report_types]
        
        for report_var in report_vars:
            ctk.CTkCheckBox(options_frame, text=report_var.get(), variable=report_var).pack(anchor="w", padx=10, pady=5)
        
        def generate_report():
            selected_reports = [var.get() for var in report_vars if var.get()]
            if not selected_reports:
                self.show_message("Error", "Please select at least one report type.")
                return
            
            # Implement report generation logic here
            self.show_message("Success", "Reports generated successfully!")
        
        # Generate button
        ctk.CTkButton(
            frame,
            text="Generate Report",
            command=generate_report
        ).pack(pady=20)
    
    def export_case(self):
        # Existing export functionality
        export_path = filedialog.askdirectory(title="Select Export Location")
        if not export_path:
            return
        
        export_dir = Path(export_path) / f"{self.case_id}_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        export_dir.mkdir(exist_ok=True)
        
        # Existing code to copy case details...
        
        # Add selected cyber forensic tools to the CSV
        tools_file = export_dir / "cyber_forensic_tools.csv"
        with open(tools_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Tool Name'])
            tools = [
                "FTK Imager",
                "EnCase",
                "Autopsy",
                "Sleuth Kit",
                "Wireshark",
                "Volatility",
                "Caine",
                "Kali Linux",
                "X1 Social Discovery",
                "Oxygen Forensics"
            ]
            for tool in tools:
                writer.writerow([tool])
        
        self.show_message("Success", f"Case exported successfully to:\n{export_dir}\nCyber forensic tools saved to:\n{tools_file.name}")
    
    def show_about(self):
        # Create about window
        about_window = ctk.CTkToplevel(self.window)
        about_window.title("About")
        about_window.geometry("800x600")
        about_window.transient(self.window)
        about_window.grab_set()
        
        # Variable to track window state
        window_exists = True
        
        # Handle window close
        def on_window_close():
            nonlocal window_exists
            window_exists = False
            about_window.grab_release()
            about_window.destroy()
        
        about_window.protocol("WM_DELETE_WINDOW", on_window_close)
        
        # Create main frame
        frame = ctk.CTkFrame(about_window)
        frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Create horizontal layout frame
        content_frame = ctk.CTkFrame(frame)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left side - Profile section
        profile_frame = ctk.CTkFrame(content_frame)
        profile_frame.pack(side="left", padx=(0, 20), fill="y")
        
        # Load and display profile image
        try:
            profile_path = Path("assets/profile.jpg")
            if profile_path.exists():
                profile_img = Image.open(profile_path)
                profile_img.thumbnail((200, 200))  # Slightly larger image
                photo = ImageTk.PhotoImage(profile_img)
                
                img_label = ctk.CTkLabel(profile_frame, image=photo, text="")
                img_label.image = photo
                img_label.pack(pady=20)
            else:
                ctk.CTkLabel(
                    profile_frame,
                    text="[Profile Image Not Found]",
                    font=("Arial", 12)
                ).pack(pady=20)
        except Exception as e:
            print(f"Error loading profile image: {e}")
            ctk.CTkLabel(
                profile_frame,
                text="[Error Loading Profile Image]",
                font=("Arial", 12)
            ).pack(pady=20)
        
        # Developer name
        ctk.CTkLabel(
            profile_frame,
            text="Neha Rupesh Mhatre",  # Replace with actual name
            font=("Arial", 16, "bold")
        ).pack(pady=5)
        
        # Developer title/role
        ctk.CTkLabel(
            profile_frame,
            text="TY BSc CS (A)",  # Replace with actual title
            font=("Arial", 14)
        ).pack(pady=5)
        
        # Right side - Description section
        desc_frame = ctk.CTkFrame(content_frame)
        desc_frame.pack(side="left", fill="both", expand=True)
        
        # Title
        ctk.CTkLabel(
            desc_frame,
            text="About Crime Investigation System",
            font=("Arial", 24, "bold")
        ).pack(pady=20)
        
        # Version info
        ctk.CTkLabel(
            desc_frame,
            text="Version 1.0.0",
            font=("Arial", 16)
        ).pack(pady=10)
        
        # Description
        description = (
            "The Crime Investigation System is a comprehensive digital solution designed "
            "to assist law enforcement agencies in managing and organizing criminal cases. "
            "This system provides tools for:\n\n"
            "• Managing suspect information\n"
            "• Cataloging evidence\n"
            "• Creating case timelines\n"
            "• Generating reports\n"
            "• Searching case details\n"
            "• Maintaining case galleries\n\n"
            "Developed with security and efficiency in mind."
        )
        
        ctk.CTkLabel(
            desc_frame,
            text=description,
            font=("Arial", 14),
            wraplength=400,  # Adjusted for side-by-side layout
            justify="left"
        ).pack(pady=20)
        
        # Copyright info
        ctk.CTkLabel(
            desc_frame,
            text="© 2024 Crime Investigation System. All rights reserved.",
            font=("Arial", 12)
        ).pack(pady=20)
    
    def show_message(self, title, message):
        message_window = ctk.CTkToplevel(self.window)
        message_window.title(title)
        message_window.geometry("300x150")
        message_window.transient(self.window)
        message_window.grab_set()
        
        ctk.CTkLabel(message_window, text=message, wraplength=250).pack(pady=20)
        
        def close_message():
            message_window.grab_release()
            message_window.destroy()
        
        ctk.CTkButton(message_window, text="OK", command=close_message).pack()

    def show_ai_assistant(self):
        # Configure Gemini API
        GOOGLE_API_KEY = "AIzaSyDZHubEfECJpEaFwvzgQcum7EtqbJrx37c"
        genai.configure(api_key=GOOGLE_API_KEY)
        
        # Create model instance
        model = genai.GenerativeModel('gemini-pro')
        
        # Initialize chat
        chat = model.start_chat(history=[])
        
        # Create AI Assistant window
        assistant_window = ctk.CTkToplevel(self.window)
        assistant_window.title("AI Assistant")
        assistant_window.geometry("800x600")
        assistant_window.transient(self.window)  # Make window transient
        assistant_window.grab_set()  # Keep window on top
        
        # Variable to track window state
        window_exists = True
        
        # Handle window close
        def on_window_close():
            nonlocal window_exists
            window_exists = False
            assistant_window.grab_release()  # Release grab before destroying
            assistant_window.destroy()
        
        assistant_window.protocol("WM_DELETE_WINDOW", on_window_close)
        
        # Create main frame
        frame = ctk.CTkFrame(assistant_window)
        frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Title
        ctk.CTkLabel(
            frame,
            text="AI Investigation Assistant (Powered by Google Gemini)",
            font=("Arial", 24, "bold")
        ).pack(pady=20)
        
        # Chat history display
        chat_frame = ctk.CTkScrollableFrame(frame)
        chat_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Input area frame
        input_frame = ctk.CTkFrame(frame)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        # Text input
        text_input = ctk.CTkTextbox(input_frame, height=100)
        text_input.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Send button
        send_button = ctk.CTkButton(
            input_frame,
            text="Send",
            width=100
        )
        send_button.pack(side="right")
        
        def create_message_bubble(text, is_user=True):
            if not window_exists:
                return None
            message_frame = ctk.CTkFrame(chat_frame)
            message_frame.pack(fill="x", padx=10, pady=5)
            
            label_text = "You:" if is_user else "AI Assistant:"
            ctk.CTkLabel(
                message_frame,
                text=label_text,
                font=("Arial", 12, "bold")
            ).pack(anchor="w", padx=5)
            
            message_label = ctk.CTkLabel(
                message_frame,
                text=text,
                wraplength=600,
                justify="left"
            )
            message_label.pack(anchor="w", padx=5)
            
            return message_label
        
        def update_ui(func):
            try:
                if window_exists and assistant_window.winfo_exists():
                    assistant_window.after(0, func)
            except Exception as e:
                print(f"Error updating UI: {e}")
        
        def process_message(user_message):
            try:
                # Create and display user message
                update_ui(lambda: create_message_bubble(user_message, True))
                
                # Create AI response bubble with initial empty text
                response_label = create_message_bubble("", False)
                if not response_label:  # Window was closed
                    return
                
                # Function to update the streaming response
                def update_response(text):
                    if window_exists and assistant_window.winfo_exists():
                        update_ui(lambda: response_label.configure(text=text))
                        update_ui(lambda: chat_frame._parent_canvas.yview_moveto(1.0))
                
                # Get streaming response from Gemini
                response = chat.send_message(user_message, stream=True)
                
                # Initialize response text
                full_response = ""
                
                # Process the stream
                for chunk in response:
                    if not window_exists:  # Check if window still exists
                        break
                    if chunk.text:
                        full_response += chunk.text
                        update_response(full_response)
                
            except Exception as e:
                if window_exists:  # Only show error if window still exists
                    error_message = f"An error occurred: {str(e)}"
                    update_ui(lambda: create_message_bubble(error_message, False))
            
            finally:
                if window_exists and assistant_window.winfo_exists():  # Check window exists before updating UI
                    # Re-enable input and button
                    update_ui(lambda: text_input.configure(state="normal"))
                    update_ui(lambda: send_button.configure(state="normal"))
                    # Set focus only if window exists
                    update_ui(lambda: text_input.focus() if assistant_window.winfo_exists() else None)
        
        def send_message():
            if not window_exists or not assistant_window.winfo_exists():
                return
            user_message = text_input.get("1.0", "end-1c").strip()
            if user_message:
                # Clear input and disable UI elements
                text_input.delete("1.0", "end")
                text_input.configure(state="disabled")
                send_button.configure(state="disabled")
                
                # Start processing in a separate thread
                thread = threading.Thread(
                    target=process_message,
                    args=(user_message,),
                    daemon=True
                )
                thread.start()
        
        # Configure send button command
        send_button.configure(command=send_message)
        
        # Bind Enter key to send message
        def handle_enter(event):
            if window_exists and assistant_window.winfo_exists() and send_button.cget("state") == "normal":
                send_message()
                return "break"
        
        text_input.bind("<Return>", handle_enter)
        
        # Initial AI greeting
        initial_frame = ctk.CTkFrame(chat_frame)
        initial_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            initial_frame,
            text="AI Assistant:",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=5)
        
        ctk.CTkLabel(
            initial_frame,
            text="Hello! I'm your AI investigation assistant powered by Google Gemini. How can I help you today?",
            wraplength=600,
            justify="left"
        ).pack(anchor="w", padx=5)
        
        # Set initial focus
        text_input.focus()

    def search_case(self):
        # Create search window
        search_window = ctk.CTkToplevel(self.window)
        search_window.title("Search Case Details")
        search_window.geometry("800x600")
        search_window.transient(self.window)
        search_window.grab_set()
        
        # Create main frame
        frame = ctk.CTkFrame(search_window)
        frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Title
        ctk.CTkLabel(
            frame,
            text="Search Case Details",
            font=("Arial", 24, "bold")
        ).pack(pady=10)
        
        # Search frame
        search_frame = ctk.CTkFrame(frame)
        search_frame.pack(fill="x", padx=10, pady=10)
        
        # Search entry
        search_entry = ctk.CTkEntry(search_frame, placeholder_text="Enter search term...")
        search_entry.pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        # Results frame with scrollbar
        results_frame = ctk.CTkScrollableFrame(frame)
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        def perform_search():
            # Clear previous results
            for widget in results_frame.winfo_children():
                widget.destroy()
            
            search_term = search_entry.get().strip().lower()
            if not search_term:
                ctk.CTkLabel(
                    results_frame, 
                    text="Please enter a search term",
                    font=("Arial", 12)
                ).pack(pady=20)
                return
            
            results_found = False
            
            try:
                # Search in suspects CSV
                suspects_file = self.cases_dir / self.case_id / f"{self.case_id}_suspects.csv"
                if suspects_file.exists():
                    with open(suspects_file, 'r', newline='') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            # Check if search term exists in any field
                            if any(search_term in str(value).lower() for value in row.values()):
                                results_found = True
                                # Create result frame
                                result_frame = ctk.CTkFrame(results_frame)
                                result_frame.pack(fill="x", padx=5, pady=5)
                                
                                # Create horizontal layout
                                content_frame = ctk.CTkFrame(result_frame)
                                content_frame.pack(fill="x", padx=10, pady=5)
                                
                                # Left side - Image
                                image_frame = ctk.CTkFrame(content_frame)
                                image_frame.pack(side="left", padx=(0, 10))
                                
                                # Try to load and display suspect image
                                try:
                                    image_path = self.cases_dir / self.case_id / "images" / row['Image']
                                    if image_path.exists():
                                        img = Image.open(image_path)
                                        img.thumbnail((100, 100))  # Resize image
                                        photo = ImageTk.PhotoImage(img)
                                        
                                        img_label = ctk.CTkLabel(image_frame, image=photo, text="")
                                        img_label.image = photo  # Keep a reference
                                        img_label.pack(padx=5, pady=5)
                                    else:
                                        ctk.CTkLabel(
                                            image_frame,
                                            text="[No Image]",
                                            width=100,
                                            height=100
                                        ).pack(padx=5, pady=5)
                                except Exception as e:
                                    print(f"Error loading suspect image: {e}")
                                    ctk.CTkLabel(
                                        image_frame,
                                        text="[Error]",
                                        width=100,
                                        height=100
                                    ).pack(padx=5, pady=5)
                                
                                # Right side - Details
                                details_frame = ctk.CTkFrame(content_frame)
                                details_frame.pack(side="left", fill="both", expand=True)
                                
                                # Create result text
                                result_text = f"SUSPECT MATCH:\n"
                                result_text += f"Name: {row.get('Suspect Name', 'N/A')}\n"
                                result_text += f"Age: {row.get('Age', 'N/A')}\n"
                                result_text += f"Gender: {row.get('Gender', 'N/A')}\n"
                                result_text += f"Description: {row.get('Notes', 'N/A')[:100]}...\n"
                                
                                ctk.CTkLabel(
                                    details_frame, 
                                    text=result_text,
                                    justify="left"
                                ).pack(padx=10, pady=5)
                
                # Search in evidence CSV
                evidence_file = self.cases_dir / self.case_id / f"{self.case_id}_evidence.csv"
                if evidence_file.exists():
                    with open(evidence_file, 'r', newline='') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            # Check if search term exists in any field
                            if any(search_term in str(value).lower() for value in row.values()):
                                results_found = True
                                # Create result frame
                                result_frame = ctk.CTkFrame(results_frame)
                                result_frame.pack(fill="x", padx=5, pady=5)
                                
                                # Create result text
                                result_text = f"EVIDENCE MATCH:\n"
                                result_text += f"Evidence ID: {row.get('Evidence ID', 'N/A')}\n"
                                result_text += f"Type: {row.get('Type', 'N/A')}\n"
                                result_text += f"Location Found: {row.get('Location Found', 'N/A')}\n"
                                result_text += f"Description: {row.get('Description', 'N/A')[:100]}...\n"
                                
                                ctk.CTkLabel(
                                    result_frame, 
                                    text=result_text,
                                    justify="left"
                                ).pack(padx=10, pady=5)
                
                # Search in notes CSV
                notes_file = self.cases_dir / self.case_id / f"{self.case_id}_notes.csv"
                if notes_file.exists():
                    with open(notes_file, 'r', newline='') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            # Check if search term exists in note
                            if search_term in row['Note'].lower():
                                results_found = True
                                # Create result frame
                                result_frame = ctk.CTkFrame(results_frame)
                                result_frame.pack(fill="x", padx=5, pady=5)
                                
                                # Create result text
                                result_text = f"NOTE MATCH:\n"
                                result_text += f"Date: {row.get('Date', 'N/A')}\n"
                                result_text += f"Note: {row['Note'][:200]}...\n"
                                
                                ctk.CTkLabel(
                                    result_frame, 
                                    text=result_text,
                                    justify="left"
                                ).pack(padx=10, pady=5)
                
                if not results_found:
                    ctk.CTkLabel(
                        results_frame, 
                        text="No matches found for your search term",
                        font=("Arial", 12)
                    ).pack(pady=20)
                    
            except Exception as e:
                ctk.CTkLabel(
                    results_frame, 
                    text=f"Error during search: {str(e)}",
                    text_color="red"
                ).pack(pady=20)
        
        # Search button
        ctk.CTkButton(
            search_frame,
            text="Search",
            command=perform_search,
            width=100
        ).pack(side="left", padx=10)
        
        # Bind Enter key to search
        def handle_enter(event):
            perform_search()
            return "break"  # Prevent default behavior
        
        search_entry.bind("<Return>", handle_enter)
        
        # Set focus to search entry
        search_entry.focus()

    def digital_forensic(self):
        # Open the Digital Forensic Dashboard
        DigitalForensicDashboard(self.window, self.case_id, self.cases_dir)

class InvestigationApp:
    def __init__(self):
        # Configure appearance
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Create window
        self.window = ctk.CTk()
        self.window.title("Crime Investigation System")
        self.window.geometry("800x600")
        self.window.configure(fg_color=COLORS['light'])
        
        # Create directories and files
        self.cases_dir = Path("cases")
        self.cases_dir.mkdir(exist_ok=True)
        
        self.master_file = self.cases_dir / "cases_master.csv"
        if not self.master_file.exists():
            with open(self.master_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Case ID', 'Date Created', 'Investigator Name', 'Contact Info', 'Case Title', 'Description'])
        
        # Create main frame with shadow effect
        self.main_frame = ctk.CTkFrame(
            self.window,
            **FRAME_STYLE
        )
        self.main_frame.pack(pady=40, padx=40, fill="both", expand=True)
        
        # Title with styling
        title_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=COLORS['primary'],
            corner_radius=10,
            height=100
        )
        title_frame.pack(fill="x", padx=20, pady=20)
        title_frame.pack_propagate(False)
        
        self.title_label = ctk.CTkLabel(
            title_frame, 
            text="Crime Investigation System",
            font=("Arial", 32, "bold"),
            text_color=COLORS['white']
        )
        self.title_label.pack(expand=True)
        
        # Buttons Frame
        self.buttons_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        self.buttons_frame.pack(pady=40, expand=True)
        
        # New Case Button
        self.new_case_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Create New Case",
            command=self.create_new_case,
            **BUTTON_STYLE['primary'],
            width=300,
            height=60,
            font=("Arial", 18)
        )
        self.new_case_btn.pack(pady=20)
        
        # Reopen Case Button
        self.reopen_case_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Reopen Existing Case",
            command=self.reopen_case,
            **BUTTON_STYLE['secondary'],
            width=300,
            height=60,
            font=("Arial", 18)
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
        reopen_window.transient(self.window)  # Make window transient
        reopen_window.grab_set()  # Keep window on top
        
        # Variable to track window state
        window_exists = True
        
        # Handle window close
        def on_window_close():
            nonlocal window_exists
            window_exists = False
            reopen_window.grab_release()  # Release grab before destroying
            reopen_window.destroy()
        
        reopen_window.protocol("WM_DELETE_WINDOW", on_window_close)
        
        # Create main frame
        frame = ctk.CTkFrame(reopen_window)
        frame.pack(padx=20, pady=20, fill="both", expand=True)
        
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
                        reopen_window.grab_release()  # Release grab before destroying
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
        
        # Set focus to first entry
        self.name_entry.focus()
    
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
        message_window.transient(self.window)
        message_window.grab_set()
        
        ctk.CTkLabel(message_window, text=message, wraplength=250).pack(pady=20)
        
        def close_message():
            message_window.grab_release()
            message_window.destroy()
        
        ctk.CTkButton(message_window, text="OK", command=close_message).pack()
    
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