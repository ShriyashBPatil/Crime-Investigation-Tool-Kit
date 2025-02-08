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
            ("🤖 AI Assistant", self.show_ai_assistant),
            ("📤 Export Case", self.export_case),
            ("ℹ️ About", self.show_about)
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
        
        # Variable to track window state
        window_exists = True
        
        # Handle window close
        def on_window_close():
            nonlocal window_exists
            window_exists = False
            notes_window.grab_release()
            notes_window.destroy()
        
        notes_window.protocol("WM_DELETE_WINDOW", on_window_close)
        
        self.show_message("Coming Soon", "Notes addition feature will be available soon!")
        
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
                                image_label = ctk.CTkLabel(suspect_item, image=photo, text="")
                                image_label.image = photo  # Keep a reference
                                image_label.pack(side="left", padx=10, pady=10)
                            
                            # Add suspect details
                            details_text = f"Name: {row.get('Suspect Name', 'N/A')}\n"
                            details_text += f"Age: {row.get('Age', 'N/A')}\n"
                            details_text += f"Gender: {row.get('Gender', 'N/A')}"
                            
                            ctk.CTkLabel(
                                suspect_item,
                                text=details_text,
                                justify="left"
                            ).pack(side="left", padx=10)
        
        # Load evidence images
        evidence_file = self.cases_dir / self.case_id / f"{self.case_id}_evidence.csv"
        if evidence_file.exists():
            with open(evidence_file, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('Images'):  # If evidence has images
                        image_list = row['Images'].split(', ')
                        evidence_item = ctk.CTkFrame(evidence_frame)
                        evidence_item.pack(fill="x", padx=10, pady=10)
                        
                        # Create a frame for images
                        images_frame = ctk.CTkFrame(evidence_item)
                        images_frame.pack(side="left", padx=10, pady=10)
                        
                        # Load and display all images for this evidence
                        for img_name in image_list:
                            image_path = self.cases_dir / self.case_id / "evidence" / row['Evidence ID'] / "images" / img_name
                            if image_path.exists():
                                photo = load_and_resize_image(image_path)
                                if photo:
                                    image_label = ctk.CTkLabel(images_frame, image=photo, text="")
                                    image_label.image = photo  # Keep a reference
                                    image_label.pack(side="left", padx=5)
                        
                        # Add evidence details
                        details_text = f"Evidence ID: {row.get('Evidence ID', 'N/A')}\n"
                        details_text += f"Type: {row.get('Type', 'N/A')}\n"
                        details_text += f"Location Found: {row.get('Location Found', 'N/A')}\n"
                        details_text += f"Date Found: {row.get('Date Found', 'N/A')}"
                        
                        ctk.CTkLabel(
                            evidence_item,
                            text=details_text,
                            justify="left"
                        ).pack(side="left", padx=10)
        
        # Add messages if no images found
        if not suspects_frame.winfo_children():
            ctk.CTkLabel(
                suspects_frame,
                text="No suspect images available",
                font=("Arial", 14)
            ).pack(pady=20)
        
        if not evidence_frame.winfo_children():
            ctk.CTkLabel(
                evidence_frame,
                text="No evidence images available",
                font=("Arial", 14)
            ).pack(pady=20)
    
    def view_timeline(self):
        timeline_window = ctk.CTkToplevel(self.window)
        timeline_window.title("Case Timeline")
        timeline_window.geometry("800x600")
        timeline_window.transient(self.window)
        timeline_window.grab_set()
        
        # Variable to track window state
        window_exists = True
        
        # Handle window close
        def on_window_close():
            nonlocal window_exists
            window_exists = False
            timeline_window.grab_release()
            timeline_window.destroy()
        
        timeline_window.protocol("WM_DELETE_WINDOW", on_window_close)
        
        self.show_message("Coming Soon", "Timeline feature will be available soon!")
        
    def generate_reports(self):
        reports_window = ctk.CTkToplevel(self.window)
        reports_window.title("Generate Reports")
        reports_window.geometry("800x600")
        reports_window.transient(self.window)
        reports_window.grab_set()
        
        # Variable to track window state
        window_exists = True
        
        # Handle window close
        def on_window_close():
            nonlocal window_exists
            window_exists = False
            reports_window.grab_release()
            reports_window.destroy()
        
        reports_window.protocol("WM_DELETE_WINDOW", on_window_close)
        
        self.show_message("Coming Soon", "Reports feature will be available soon!")
        
    def search_case(self):
        # Create search window
        search_window = ctk.CTkToplevel(self.window)
        search_window.title("Search Case Details")
        search_window.geometry("800x600")
        search_window.transient(self.window)
        search_window.grab_set()
        
        # Variable to track window state
        window_exists = True
        
        # Handle window close
        def on_window_close():
            nonlocal window_exists
            window_exists = False
            search_window.grab_release()
            search_window.destroy()
        
        search_window.protocol("WM_DELETE_WINDOW", on_window_close)
        
        # Create main frame
        frame = ctk.CTkFrame(search_window)
        frame.pack(padx=20, pady=20, fill="both", expand=True)
        
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
                                result_text += f"Suspect ID: {row.get('Suspect Name', 'N/A')}\n"
                                result_text += f"Name: {row.get('Suspect Name', 'N/A')}\n"
                                result_text += f"Age: {row.get('Age', 'N/A')}\n"
                                result_text += f"Description: {row.get('Notes', 'N/A')}\n"
                                
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
                                
                                # Create horizontal layout
                                content_frame = ctk.CTkFrame(result_frame)
                                content_frame.pack(fill="x", padx=10, pady=5)
                                
                                # Left side - Image
                                image_frame = ctk.CTkFrame(content_frame)
                                image_frame.pack(side="left", padx=(0, 10))
                                
                                # Try to load and display evidence image
                                try:
                                    image_path = self.cases_dir / self.case_id / "evidence" / row['Evidence ID'] / "images" / row['Images'].split(', ')[0]
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
                                    print(f"Error loading evidence image: {e}")
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
                                result_text = f"EVIDENCE MATCH:\n"
                                result_text += f"Evidence ID: {row.get('Evidence ID', 'N/A')}\n"
                                result_text += f"Type: {row.get('Type', 'N/A')}\n"
                                result_text += f"Location Found: {row.get('Location Found', 'N/A')}\n"
                                result_text += f"Date Found: {row.get('Date Found', 'N/A')}\n"
                                result_text += f"Found By: {row.get('Found By', 'N/A')}\n"
                                
                                ctk.CTkLabel(
                                    details_frame, 
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
        
        # Set focus to search entry
        search_entry.focus()
    
    def export_case(self):
        export_window = ctk.CTkToplevel(self.window)
        export_window.title("Export Case")
        export_window.geometry("800x600")
        export_window.transient(self.window)
        export_window.grab_set()
        
        # Variable to track window state
        window_exists = True
        
        # Handle window close
        def on_window_close():
            nonlocal window_exists
            window_exists = False
            export_window.grab_release()
            export_window.destroy()
        
        export_window.protocol("WM_DELETE_WINDOW", on_window_close)
        
        self.show_message("Coming Soon", "Export feature will be available soon!")
    
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
        
        # Variable to track window state
        window_exists = True
        
        # Handle window close
        def on_window_close():
            nonlocal window_exists
            window_exists = False
            message_window.grab_release()
            message_window.destroy()
        
        message_window.protocol("WM_DELETE_WINDOW", on_window_close)
        
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
        
        # Variable to track window state
        window_exists = True
        
        # Handle window close
        def on_window_close():
            nonlocal window_exists
            window_exists = False
            message_window.grab_release()
            message_window.destroy()
        
        message_window.protocol("WM_DELETE_WINDOW", on_window_close)
        
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