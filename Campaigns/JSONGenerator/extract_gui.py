"""
Simple GUI for Campaign Content Extractor
Double-click this file to run with a friendly interface!
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import threading
import sys
import re
import subprocess
import os

from extract_to_google_sheets import CampaignExtractor, GoogleSheetsExporter


class ExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Campaign Content Extractor")
        
        # Optimized for laptop screens (550px height fits comfortably on 768px laptop screens)
        self.root.geometry("820x550")
        
        # Make window resizable but set minimum size
        self.root.minsize(750, 450)
        
        # Set UTF-8 encoding
        if sys.platform == 'win32':
            try:
                sys.stdout.reconfigure(encoding='utf-8')
            except:
                pass
        
        # Store dynamic campaign name fields
        self.dynamic_campaign_fields = []
        self.assessed_emails = []
        
        # Create main scrollable container
        self.create_scrollable_container()
        self.create_widgets()
        self.auto_find_document()
    
    def create_scrollable_container(self):
        """Create a scrollable canvas for the entire GUI"""
        # Create main canvas with scrollbar
        self.main_canvas = tk.Canvas(self.root, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.main_canvas)
        
        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        
        self.canvas_frame = self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack canvas and scrollbar
        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind canvas resize to update scroll region
        self.main_canvas.bind('<Configure>', self._on_canvas_configure)
        
        # Enable mouse wheel scrolling
        self.main_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def _on_canvas_configure(self, event):
        """Update scrollable frame width when canvas is resized"""
        self.main_canvas.itemconfig(self.canvas_frame, width=event.width)
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def create_widgets(self):
        """Create the GUI layout"""
        
        # Title (ultra-compact for laptop screens)
        title = tk.Label(
            self.scrollable_frame, 
            text="Campaign Content Extractor",
            font=("Arial", 12, "bold"),
            pady=3
        )
        title.pack()
        
        features = tk.Label(
            self.scrollable_frame,
            text="Word docs → Google Sheets  |  ✓ Color ✓ Checkbox ✓ Auto Upload",
            font=("Arial", 8),
            fg="gray"
        )
        features.pack(pady=1)
        
        # Document Selection Frame (minimal padding for laptop screens)
        doc_frame = ttk.LabelFrame(self.scrollable_frame, text="1. Select Word Document", padding=3)
        doc_frame.pack(fill="x", padx=10, pady=3)
        
        self.doc_path_var = tk.StringVar()
        doc_entry = ttk.Entry(doc_frame, textvariable=self.doc_path_var, width=50)
        doc_entry.pack(side="left", padx=5)
        
        browse_btn = ttk.Button(doc_frame, text="Browse...", command=self.browse_document)
        browse_btn.pack(side="left", padx=2)
        
        # NEW: Assess Document button
        self.assess_btn = ttk.Button(doc_frame, text="Assess Document", command=self.assess_document)
        self.assess_btn.pack(side="left", padx=2)
        
        # Assessment Results Frame (initially hidden, will show after assess)
        self.assessment_frame = ttk.LabelFrame(self.scrollable_frame, text="2. Document Assessment & Campaign Names", padding=3)
        # Don't pack yet - will pack when user clicks Assess
        
        self.assessment_label = tk.Label(
            self.assessment_frame, 
            text="Click 'Assess Document' to scan for email templates",
            justify="left",
            font=("Arial", 8),
            fg="gray"
        )
        self.assessment_label.pack(fill="x", pady=(0, 5))
        
        # Dynamic Campaign Name fields container
        self.dynamic_fields_frame = ttk.Frame(self.assessment_frame)
        self.dynamic_fields_frame.pack(fill="both", expand=True)
        
        # Metadata Frame (additional fields - compact)
        self.meta_frame = ttk.LabelFrame(self.scrollable_frame, text="3. Additional Metadata", padding=3)
        self.meta_frame.pack(fill="x", padx=10, pady=3)
        
        # Language (compact)
        tk.Label(self.meta_frame, text="Language:", font=("Arial", 8)).grid(row=0, column=0, sticky="w", pady=2)
        self.language_var = tk.StringVar(value="en-us")
        lang_combo = ttk.Combobox(self.meta_frame, textvariable=self.language_var, width=15, values=["en-us", "en-es"])
        lang_combo.grid(row=0, column=1, sticky="w", pady=2, padx=5)
        
        # URL/UTM
        tk.Label(self.meta_frame, text="URL/UTM:", font=("Arial", 8)).grid(row=1, column=0, sticky="w", pady=2)
        self.url_var = tk.StringVar()
        ttk.Entry(self.meta_frame, textvariable=self.url_var, width=45).grid(row=1, column=1, pady=2, padx=5)
        
        # Sponsor
        tk.Label(self.meta_frame, text="Sponsor:", font=("Arial", 8)).grid(row=2, column=0, sticky="w", pady=2)
        self.sponsor_var = tk.StringVar(value="Takeda")
        ttk.Entry(self.meta_frame, textvariable=self.sponsor_var, width=45).grid(row=2, column=1, pady=2, padx=5)
        
        # Extract Button (compact)
        extract_frame = tk.Frame(self.scrollable_frame)
        extract_frame.pack(pady=5)
        
        self.extract_btn = ttk.Button(
            extract_frame,
            text="4. Extract Content",
            command=self.extract_content,
            style="Accent.TButton"
        )
        self.extract_btn.pack()
        
        # Progress
        self.progress = ttk.Progressbar(self.scrollable_frame, mode='indeterminate', length=300)
        self.progress.pack(pady=3)
        
        # Output Text (compact - smaller for laptop screens)
        output_frame = ttk.LabelFrame(self.scrollable_frame, text="Output Log", padding=3)
        output_frame.pack(fill="both", expand=True, padx=10, pady=3)
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            height=8,  # Reduced to 8 lines for laptop screens
            width=95,
            font=("Consolas", 8),
            wrap=tk.WORD
        )
        self.output_text.pack(fill="both", expand=True)
        
        # Status bar (fixed at bottom of main window, not scrollable_frame)
        self.status_var = tk.StringVar(value="Ready to extract")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bd=1,
            relief="sunken",
            anchor="w",
            font=("Arial", 8)
        )
        status_bar.pack(side="bottom", fill="x")
    
    def auto_find_document(self):
        """Automatically find Word documents in current directory"""
        docx_files = list(Path(".").glob("*.docx"))
        if docx_files:
            self.doc_path_var.set(str(docx_files[0]))
            self.log(f"Found document: {docx_files[0].name}")
    
    def browse_document(self):
        """Browse for Word document"""
        filename = filedialog.askopenfilename(
            title="Select Word Document",
            filetypes=[("Word Documents", "*.docx"), ("All Files", "*.*")]
        )
        if filename:
            self.doc_path_var.set(filename)
            self.log(f"Selected: {Path(filename).name}")
    
    def assess_document(self):
        """Assess the document and create dynamic Campaign Name fields per email"""
        doc_path = self.doc_path_var.get()
        
        if not doc_path or not Path(doc_path).exists():
            messagebox.showwarning("No Document", "Please select a document first!")
            return
        
        try:
            self.log("=" * 80)
            self.log("ASSESSING DOCUMENT...")
            self.log("=" * 80)
            
            # Extract email headers and smart defaults
            extractor = CampaignExtractor(doc_path)
            
            # Get smart defaults from document
            self.log("\nExtracting smart defaults from document...")
            filename_stem = Path(doc_path).stem.replace('_', ' ').replace('-', ' ')
            smart_defaults = extractor.extract_smart_defaults_from_document()
            
            self.log("  Smart defaults detected:")
            if smart_defaults.get('Campaign Name'):
                self.log(f"    Campaign Name: {smart_defaults['Campaign Name']}")
            if smart_defaults.get('Sponsor'):
                self.log(f"    Sponsor: {smart_defaults['Sponsor']}")
            if smart_defaults.get('Language'):
                self.log(f"    Language: {smart_defaults['Language']}")
            if smart_defaults.get('URL/UTM'):
                self.log(f"    URL/UTM: {smart_defaults['URL/UTM']}")
            
            # Update GUI metadata fields with smart defaults
            if smart_defaults.get('Language'):
                self.root.after(0, lambda: self.language_var.set(smart_defaults['Language']))
            if smart_defaults.get('URL/UTM'):
                self.root.after(0, lambda: self.url_var.set(smart_defaults['URL/UTM']))
            if smart_defaults.get('Sponsor'):
                self.root.after(0, lambda: self.sponsor_var.set(smart_defaults['Sponsor']))
            
            email_headers = extractor.extract_email_headers_from_doc()
            
            if not email_headers:
                messagebox.showinfo(
                    "No Email Templates Found",
                    "Could not find email template headers in the document.\n\n"
                    "Looking for headers like:\n"
                    "  • Email 1: Long-form email\n"
                    "  • Email 2: Short reminder\n\n"
                    "The document may have a different structure."
                )
                self.log("  Warning: No email headers found")
                return
            
            # Parse email headers to extract message names
            self.assessed_emails = []
            for email_num, header_text in sorted(email_headers.items()):
                # Keep full header text as message name ("Email 1: Long-form email")
                match = re.match(r'Email\s+(\d+):\s*(.+)', header_text, re.IGNORECASE)
                if match:
                    email_id = match.group(1)
                    message_name = header_text  # Keep full text including "Email 1:"
                else:
                    email_id = str(email_num)
                    message_name = header_text
                
                self.assessed_emails.append({
                    'email_id': email_id,
                    'message_name': message_name,
                    'header_text': header_text
                })
                
                self.log(f"  Email {email_id}: {message_name}")
            
            # NEW: Detect images in document
            self.log("\nDetecting images in document...")
            detected_images = extractor.detect_images_in_document()
            
            if detected_images:
                preferred_count = sum(1 for img in detected_images if img.get('preferred', False))
                self.log(f"  Found {len(detected_images)} image(s):")
                for img in detected_images:
                    preferred_mark = " [X] PREFERRED" if img.get('preferred', False) else ""
                    self.log(f"     {img['filename']} ({img['format']}, {img['size_kb']} KB){preferred_mark}")
                if preferred_count > 0:
                    self.log(f"  -> {preferred_count} image(s) marked as preferred with [X]")
                
                # Store images for later use
                self.detected_images = detected_images
                
                # Show image options frame
                self.show_image_options(len(detected_images))
            else:
                self.log("  No images detected in document")
                self.detected_images = []
            
            # NEW: Check Git prerequisites for auto-upload
            self.git_status = self.check_git_prerequisites()
            
            # Show warning dialog if Git issues found
            if self.git_status['errors']:
                error_msg = "Git Auto-Upload Not Available:\n\n"
                for error in self.git_status['errors']:
                    error_msg += f"  • {error}\n"
                error_msg += "\nImages will be saved locally but not auto-uploaded to GitHub."
                error_msg += "\n\nFix Git issues to enable auto-upload."
                
                messagebox.showwarning("Git Setup Required", error_msg)
            
            elif self.git_status['warnings']:
                # Don't block with dialog, just log warnings
                self.log("\n" + "!"*80)
                self.log("Git Warnings:")
                for warning in self.git_status['warnings']:
                    self.log(f"  ! {warning}")
                self.log("  Auto-upload may work with limitations.")
                self.log("!"*80)
            
            # Show assessment frame
            # Pack it before the metadata frame
            self.assessment_frame.pack(fill="x", padx=10, pady=3, before=self.meta_frame)
            
            # Update assessment label
            count = len(self.assessed_emails)
            if count == 1:
                summary = f"✅ Found 1 email template:\n   • {self.assessed_emails[0]['message_name']}"
            else:
                summary = f"✅ Found {count} email templates:\n"
                for email in self.assessed_emails:
                    summary += f"   • Email {email['email_id']}: {email['message_name']}\n"
            
            self.assessment_label.config(text=summary, fg="green")
            
            # Clear previous dynamic fields
            for widget in self.dynamic_fields_frame.winfo_children():
                widget.destroy()
            self.dynamic_campaign_fields.clear()
            
            # Create dynamic Campaign Name fields
            if count == 1:
                # Single email - simple layout
                info = tk.Label(
                    self.dynamic_fields_frame,
                    text="Enter Campaign Name for this email:",
                    font=("Arial", 8, "bold")
                )
                info.pack(anchor="w", pady=(3, 5))
                
                email = self.assessed_emails[0]
                field_frame = ttk.Frame(self.dynamic_fields_frame)
                field_frame.pack(fill="x", pady=5)
                
                tk.Label(
                    field_frame, 
                    text=f"📧 {email['message_name']}:", 
                    width=30, 
                    anchor="w"
                ).pack(side="left")
                
                campaign_var = tk.StringVar(value=smart_defaults.get('Campaign Name', filename_stem))
                ttk.Entry(field_frame, textvariable=campaign_var, width=50).pack(side="left", padx=5)
                
                self.dynamic_campaign_fields.append({
                    'message_name': email['message_name'],
                    'campaign_var': campaign_var
                })
            else:
                # Multiple emails - show all with separate fields
                info = tk.Label(
                    self.dynamic_fields_frame,
                    text="Enter Campaign Name for each email template:",
                    font=("Arial", 8, "bold")
                )
                info.pack(anchor="w", pady=(3, 5))
                
                for idx, email in enumerate(self.assessed_emails, 1):
                    field_frame = ttk.Frame(self.dynamic_fields_frame)
                    field_frame.pack(fill="x", pady=5)
                    
                    label_text = f"📧 Email {email['email_id']}: {email['message_name']}"
                    tk.Label(field_frame, text=label_text, width=40, anchor="w").pack(side="left")
                    
                    # Default: use smart default from document, or append number
                    smart_campaign_name = smart_defaults.get('Campaign Name', filename_stem)
                    if idx == 1:
                        default_name = smart_campaign_name
                    else:
                        default_name = f"{smart_campaign_name} (Email {idx})"
                    
                    campaign_var = tk.StringVar(value=default_name)
                    ttk.Entry(field_frame, textvariable=campaign_var, width=45).pack(side="left", padx=5)
                    
                    self.dynamic_campaign_fields.append({
                        'message_name': email['message_name'],
                        'campaign_var': campaign_var
                    })
            
            self.log(f"\n✅ Assessment complete! Found {count} email template(s)")
            self.log("   Campaign Name fields created. Edit as needed, then click 'Extract Content'")
            self.log("=" * 80)
            
            messagebox.showinfo(
                "Assessment Complete",
                f"✅ Found {count} email template{'s' if count != 1 else ''}!\n\n"
                f"Campaign Name fields have been created below.\n"
                f"Review and edit as needed, then click 'Extract Content'."
            )
            
        except Exception as e:
            error_msg = f"Error assessing document: {str(e)}"
            self.log(f"\n[ERROR] {error_msg}")
            messagebox.showerror("Assessment Error", error_msg)
            import traceback
            traceback.print_exc()
    
    def show_image_options(self, image_count):
        """Display image upload options after assessment"""
        
        # Create or update image options frame
        if not hasattr(self, 'image_options_frame'):
            self.image_options_frame = ttk.LabelFrame(
                self.scrollable_frame, 
                text="Image Upload Options", 
                padding=3
            )
            self.image_options_frame.pack(fill="x", padx=10, pady=3, before=self.meta_frame)
        
        # Clear previous content
        for widget in self.image_options_frame.winfo_children():
            widget.destroy()
        
        # Image count label (compact)
        count_label = tk.Label(
            self.image_options_frame,
            text=f"Found {image_count} image(s) in document",
            font=("Arial", 8, "bold"),
            fg="green"
        )
        count_label.pack(anchor="w", pady=(0, 3))
        
        # Radio buttons for upload options
        self.image_upload_option = tk.StringVar(value="all")
        
        options_frame = tk.Frame(self.image_options_frame)
        options_frame.pack(fill="x", pady=3)
        
        tk.Radiobutton(
            options_frame,
            text="Upload all images to GitHub automatically",
            variable=self.image_upload_option,
            value="all",
            font=("Arial", 8)
        ).pack(anchor="w", pady=1)
        
        tk.Radiobutton(
            options_frame,
            text="Upload preferred images only (marked with [X] in doc)",
            variable=self.image_upload_option,
            value="select",
            command=self.show_image_selector,
            font=("Arial", 8)
        ).pack(anchor="w", pady=1)
        
        tk.Radiobutton(
            options_frame,
            text="Skip image upload (I'll handle manually)",
            variable=self.image_upload_option,
            value="skip",
            font=("Arial", 8)
        ).pack(anchor="w", pady=1)
        
        # Preview button (compact)
        preview_btn = ttk.Button(
            self.image_options_frame,
            text="Preview Detected Images",
            command=self.preview_images
        )
        preview_btn.pack(pady=(5, 0))
    
    def show_image_selector(self):
        """Show a window for selecting specific images"""
        if not hasattr(self, 'detected_images') or not self.detected_images:
            return
        
        # Create selector window
        selector = tk.Toplevel(self.root)
        selector.title("Select Images to Upload")
        selector.geometry("500x400")
        
        tk.Label(
            selector,
            text="Review and select images to upload to GitHub:",
            font=("Arial", 11, "bold"),
            pady=10
        ).pack()
        
        # Show preferred count
        preferred_count = sum(1 for img in self.detected_images if img.get('preferred', False))
        if preferred_count > 0:
            tk.Label(
                selector,
                text=f"{preferred_count} image(s) marked as PREFERRED with [X] in document",
                font=("Arial", 9),
                fg="green",
                pady=5
            ).pack()
        
        # Scrollable frame for checkboxes
        canvas = tk.Canvas(selector)
        scrollbar = ttk.Scrollbar(selector, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create checkbox for each image
        self.image_checkboxes = []
        for img in self.detected_images:
            # Pre-select only preferred images
            is_preferred = img.get('preferred', False)
            var = tk.BooleanVar(value=is_preferred)
            
            # Add preferred indicator to label
            preferred_mark = " [X] PREFERRED" if is_preferred else ""
            cb = tk.Checkbutton(
                scrollable_frame,
                text=f"  {img['filename']} ({img['format']}, {img['size_kb']} KB){preferred_mark}",
                variable=var,
                font=("Arial", 9),
                fg="green" if is_preferred else "black"
            )
            cb.pack(anchor="w", pady=2, padx=20)
            self.image_checkboxes.append((img, var))
        
        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")
        
        # Confirm button
        def confirm_selection():
            for img, var in self.image_checkboxes:
                img['selected'] = var.get()
            selector.destroy()
            selected_count = sum(1 for img in self.detected_images if img['selected'])
            self.log(f"  User selected {selected_count}/{len(self.detected_images)} image(s) for upload")
        
        ttk.Button(
            selector,
            text="Confirm Selection",
            command=confirm_selection
        ).pack(pady=10)
    
    def preview_images(self):
        """Show preview of detected images with details"""
        if not hasattr(self, 'detected_images') or not self.detected_images:
            messagebox.showinfo("No Images", "No images detected yet. Click 'Assess Document' first.")
            return
        
        preview = tk.Toplevel(self.root)
        preview.title("Image Preview")
        preview.geometry("600x500")
        
        tk.Label(
            preview,
            text=f"Detected Images ({len(self.detected_images)} total)",
            font=("Arial", 12, "bold"),
            pady=10
        ).pack()
        
        # Create scrollable text widget for image list
        text = scrolledtext.ScrolledText(preview, height=20, width=70, font=("Consolas", 9))
        text.pack(fill="both", expand=True, padx=10, pady=10)
        
        for img in self.detected_images:
            preferred_mark = " [X] PREFERRED" if img.get('preferred', False) else ""
            text.insert("end", f"{img['filename']}{preferred_mark}\n")
            text.insert("end", f"   Format: {img['format']}\n")
            text.insert("end", f"   Size: {img['size_kb']} KB\n")
            if img.get('context'):
                text.insert("end", f"   Context: {img['context']}\n")
            text.insert("end", f"   Status: {'Selected' if img.get('selected', True) else 'Skipped'}\n")
            text.insert("end", "\n")
        
        text.config(state="disabled")
        
        ttk.Button(preview, text="Close", command=preview.destroy).pack(pady=5)
    
    def check_git_prerequisites(self):
        """
        Check if Git is properly configured for auto-upload.
        Returns: dict with status and messages
        """
        git_status = {
            'git_installed': False,
            'is_repo': False,
            'has_remote': False,
            'can_commit': False,
            'warnings': [],
            'errors': []
        }
        
        try:
            # Check 1: Git installed
            self.log("\nChecking Git prerequisites for auto-upload...")
            try:
                result = subprocess.run(
                    ['git', '--version'],
                    capture_output=True,
                    text=True,
                    cwd=Path.cwd(),
                    timeout=5
                )
                if result.returncode == 0:
                    git_status['git_installed'] = True
                    git_version = result.stdout.strip()
                    self.log(f"  [OK] Git installed: {git_version}")
                else:
                    git_status['errors'].append("Git not found")
                    self.log("  [X] Git not found")
                    return git_status
            except (FileNotFoundError, subprocess.TimeoutExpired):
                git_status['errors'].append("Git not installed")
                self.log("  [X] Git not installed")
                self.log("      Install from: https://git-scm.com/downloads")
                return git_status
            
            # Check 2: Is Git repository
            result = subprocess.run(
                ['git', 'rev-parse', '--git-dir'],
                capture_output=True,
                text=True,
                cwd=Path.cwd(),
                timeout=5
            )
            if result.returncode == 0:
                git_status['is_repo'] = True
                self.log("  [OK] Git repository initialized")
            else:
                git_status['errors'].append("Not a Git repository")
                self.log("  [X] Not a Git repository")
                self.log("      Run: git init")
                return git_status
            
            # Check 3: Has remote configured
            result = subprocess.run(
                ['git', 'remote', '-v'],
                capture_output=True,
                text=True,
                cwd=Path.cwd(),
                timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                git_status['has_remote'] = True
                remote_lines = result.stdout.strip().split('\n')
                remote_name = remote_lines[0].split()[0] if remote_lines else "origin"
                self.log(f"  [OK] Git remote configured: {remote_name}")
            else:
                git_status['warnings'].append("No Git remote configured")
                self.log("  [!] No Git remote configured")
                self.log("      Images will be committed locally only")
                self.log("      To add remote: git remote add origin [URL]")
            
            # Check 4: Can commit (user.name and user.email configured)
            result = subprocess.run(
                ['git', 'config', 'user.name'],
                capture_output=True,
                text=True,
                cwd=Path.cwd(),
                timeout=5
            )
            has_name = result.returncode == 0 and result.stdout.strip()
            
            result = subprocess.run(
                ['git', 'config', 'user.email'],
                capture_output=True,
                text=True,
                cwd=Path.cwd(),
                timeout=5
            )
            has_email = result.returncode == 0 and result.stdout.strip()
            
            if has_name and has_email:
                git_status['can_commit'] = True
                self.log("  [OK] Git user configured")
            else:
                git_status['warnings'].append("Git user not configured")
                self.log("  [!] Git user not fully configured")
                if not has_name:
                    self.log('      Run: git config user.name "Your Name"')
                if not has_email:
                    self.log('      Run: git config user.email "your.email@example.com"')
            
            # Check 5: Check for uncommitted changes (optional warning)
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True,
                cwd=Path.cwd(),
                timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                uncommitted_count = len(result.stdout.strip().split('\n'))
                git_status['warnings'].append(f"{uncommitted_count} uncommitted changes")
                self.log(f"  [!] {uncommitted_count} uncommitted file(s) in repository")
                self.log("      Consider committing before adding images")
            
            # Summary
            if git_status['git_installed'] and git_status['is_repo']:
                if git_status['has_remote']:
                    self.log("\n  >> Git auto-upload ready!")
                else:
                    self.log("\n  >> Git setup complete but no remote - images will commit locally only")
            
        except Exception as e:
            git_status['errors'].append(f"Error checking Git: {str(e)}")
            self.log(f"  [X] Error checking Git: {str(e)}")
        
        return git_status
    
    def get_github_repo_url(self):
        """
        Extract GitHub repository URL from Git remote.
        Returns: tuple of (username, repo_name) or (None, None)
        """
        try:
            result = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                capture_output=True,
                text=True,
                cwd=Path.cwd(),
                timeout=5
            )
            
            if result.returncode == 0:
                remote_url = result.stdout.strip()
                
                # Parse GitHub URL - handle both HTTPS and SSH formats
                # HTTPS: https://github.com/username/repo.git
                # SSH: git@github.com:username/repo.git
                
                if 'github.com' in remote_url:
                    if remote_url.startswith('https://'):
                        # HTTPS format
                        parts = remote_url.replace('https://github.com/', '').replace('.git', '').split('/')
                        if len(parts) >= 2:
                            return parts[0], parts[1]
                    elif remote_url.startswith('git@'):
                        # SSH format
                        parts = remote_url.replace('git@github.com:', '').replace('.git', '').split('/')
                        if len(parts) >= 2:
                            return parts[0], parts[1]
                
                self.log(f"  Note: Could not parse GitHub URL: {remote_url}")
                return None, None
            
        except Exception as e:
            self.log(f"  Note: Could not get GitHub repo URL: {e}")
        
        return None, None
    
    def generate_github_image_urls(self, image_filenames, username, repo_name, branch='main'):
        """
        Generate GitHub raw URLs for images.
        Returns: dict mapping filename to URL
        """
        urls = {}
        base_url = f"https://raw.githubusercontent.com/{username}/{repo_name}/{branch}/campaign_images"
        
        for filename in image_filenames:
            image_name = Path(filename).name
            urls[image_name] = f"{base_url}/{image_name}"
        
        return urls
    
    def update_rows_with_image_urls(self, rows, image_urls):
        """
        Update rows with GitHub image URLs in Hero Image (URL) column.
        Handles multiple rows (multiple emails).
        """
        if not image_urls:
            return rows
        
        # Get all image URLs as a list
        url_list = list(image_urls.values())
        
        for idx, row in enumerate(rows):
            # If there are multiple images and multiple rows, try to match them
            if idx < len(url_list):
                # Single image per email
                row['Hero Image (URL)'] = url_list[idx]
            elif len(url_list) == 1:
                # Same image for all emails
                row['Hero Image (URL)'] = url_list[0]
            elif len(url_list) > 0:
                # Multiple images, use first as default
                row['Hero Image (URL)'] = url_list[0]
            
            # Log with truncation for readability
            url_preview = row.get('Hero Image (URL)', 'No URL')
            if len(url_preview) > 60:
                url_preview = url_preview[:60] + "..."
            self.log(f"  Updated row {idx+1}: {url_preview}")
        
        return rows
    
    def log(self, message):
        """Add message to output text"""
        self.output_text.insert("end", message + "\n")
        self.output_text.see("end")
        self.root.update()
    
    def auto_upload_to_github(self, saved_files, campaign_name="campaign"):
        """
        Automatically upload images to GitHub using Git commands.
        Returns: tuple of (success: bool, image_urls: dict)
        """
        try:
            # Get the project root directory
            project_root = Path.cwd()
            
            self.log("\n" + "="*80)
            self.log("UPLOADING TO GITHUB")
            self.log("="*80)
            self.log(f"\nProject directory: {project_root}")
            
            # Check if git is available
            self.log("\n[1/4] Checking Git installation...")
            try:
                result = subprocess.run(
                    ['git', '--version'],
                    capture_output=True,
                    text=True,
                    cwd=project_root
                )
                if result.returncode == 0:
                    self.log(f"  Git found: {result.stdout.strip()}")
                else:
                    self.log("  ERROR: Git not found. Please install Git or use manual upload.")
                    return False, {}
            except FileNotFoundError:
                self.log("  ERROR: Git not found. Please install Git or use manual upload.")
                return False, {}
            
            # Check if we're in a git repository
            self.log("\n[2/4] Checking Git repository...")
            result = subprocess.run(
                ['git', 'status'],
                capture_output=True,
                text=True,
                cwd=project_root
            )
            if result.returncode != 0:
                self.log("  ERROR: Not a Git repository. Initialize Git first or use manual upload.")
                return False, {}
            self.log("  Repository status: OK")
            
            # Add files
            self.log("\n[3/4] Adding images to Git...")
            result = subprocess.run(
                ['git', 'add', 'campaign_images/'],
                capture_output=True,
                text=True,
                cwd=project_root
            )
            if result.returncode != 0:
                self.log(f"  ERROR adding files: {result.stderr}")
                return False, {}
            self.log(f"  Added {len(saved_files)} file(s) to Git staging")
            
            # Commit
            self.log("\n[4/4] Committing and pushing to GitHub...")
            commit_message = f"Add campaign images: {campaign_name}"
            result = subprocess.run(
                ['git', 'commit', '-m', commit_message],
                capture_output=True,
                text=True,
                cwd=project_root
            )
            
            # Check if there were changes to commit
            if "nothing to commit" in result.stdout or "nothing added to commit" in result.stdout:
                self.log("  No new changes to commit (images may already be in repository)")
            elif result.returncode != 0:
                self.log(f"  Warning: {result.stderr}")
            else:
                self.log(f"  Committed: {commit_message}")
            
            # Push to GitHub
            self.log("  Pushing to GitHub...")
            result = subprocess.run(
                ['git', 'push'],
                capture_output=True,
                text=True,
                cwd=project_root,
                timeout=30  # 30 second timeout
            )
            
            if result.returncode == 0:
                self.log("\n" + "="*80)
                self.log("SUCCESS: Images uploaded to GitHub!")
                self.log("="*80)
                
                # Generate GitHub URLs for the uploaded images
                username, repo_name = self.get_github_repo_url()
                
                if username and repo_name:
                    self.log(f"\nGenerating image URLs for: {username}/{repo_name}")
                    image_urls = self.generate_github_image_urls(saved_files, username, repo_name)
                    
                    self.log("\nGenerated GitHub URLs:")
                    for filename, url in image_urls.items():
                        self.log(f"  {filename}")
                        self.log(f"    -> {url}")
                    
                    return True, image_urls
                else:
                    self.log("\nYour images are now available at:")
                    self.log("  https://github.com/[your-repo]/campaign_images/")
                    
                    # List uploaded files
                    self.log("\nUploaded files:")
                    for filepath in saved_files:
                        filename = Path(filepath).name
                        self.log(f"  - {filename}")
                    
                    self.log("\n  Note: Could not determine GitHub repo for URL generation")
                    self.log("  You can manually add image URLs to spreadsheet")
                    return True, {}
            else:
                error_msg = result.stderr.strip()
                if "no upstream branch" in error_msg.lower():
                    self.log("\n  Setting upstream branch and pushing...")
                    result = subprocess.run(
                        ['git', 'push', '--set-upstream', 'origin', 'main'],
                        capture_output=True,
                        text=True,
                        cwd=project_root,
                        timeout=30
                    )
                    if result.returncode == 0:
                        self.log("\nSUCCESS: Images uploaded to GitHub!")
                        
                        # Generate GitHub URLs
                        username, repo_name = self.get_github_repo_url()
                        if username and repo_name:
                            image_urls = self.generate_github_image_urls(saved_files, username, repo_name)
                            self.log("\nGenerated GitHub URLs (see above for details)")
                            return True, image_urls
                        return True, {}
                
                self.log(f"\n  ERROR pushing to GitHub: {error_msg}")
                self.log("\nFallback: Use GitHub Desktop or manual commands:")
                self.log("  git add campaign_images/")
                self.log(f"  git commit -m '{commit_message}'")
                self.log("  git push")
                return False, {}
                
        except subprocess.TimeoutExpired:
            self.log("\n  ERROR: Git push timed out. Check your internet connection.")
            self.log("  Try manual upload or check GitHub authentication.")
            return False, {}
        except Exception as e:
            self.log(f"\n  ERROR during GitHub upload: {str(e)}")
            self.log("\nFallback: Use manual upload")
            self.log("  1. Open GitHub Desktop")
            self.log("  2. Commit the campaign_images folder")
            self.log("  3. Push to origin")
            return False, {}
    
    def extract_content(self):
        """Extract content from Word document"""
        doc_path = self.doc_path_var.get()
        
        if not doc_path or not Path(doc_path).exists():
            messagebox.showerror("Error", "Please select a valid Word document")
            return
        
        # Disable button and start progress
        self.extract_btn.config(state="disabled")
        self.progress.start()
        self.output_text.delete("1.0", "end")
        self.status_var.set("Extracting...")
        
        # Run extraction in thread to keep GUI responsive
        thread = threading.Thread(target=self._do_extraction, daemon=True)
        thread.start()
    
    def _do_extraction(self):
        """Actual extraction work (runs in thread)"""
        try:
            doc_path = self.doc_path_var.get()
            
            self.log("=" * 80)
            self.log("EXTRACTING CAMPAIGN CONTENT")
            self.log("=" * 80)
            self.log(f"\nDocument: {Path(doc_path).name}")
            
            extractor = CampaignExtractor(doc_path)
            
            # Check if we have dynamic campaign fields (from Assess button)
            if self.dynamic_campaign_fields:
                self.log(f"\nUsing assessed email templates ({len(self.dynamic_campaign_fields)} found):")
                
                # Base metadata (applies to all emails)
                base_metadata = {
                    'Language': self.language_var.get().strip(),
                    'URL/UTM': self.url_var.get().strip(),
                    'End Matter (Enter Sponsor)': self.sponsor_var.get().strip()
                }
                
                # Extract each email with its specific Campaign Name
                all_rows = []
                emails = extractor.detect_email_sections()
                
                for idx, (email_info, campaign_field) in enumerate(zip(emails, self.dynamic_campaign_fields)):
                    # Get Campaign Name from the corresponding field
                    campaign_name = campaign_field['campaign_var'].get().strip()
                    message_name = campaign_field['message_name']
                    
                    self.log(f"\n  Email {idx+1}:")
                    self.log(f"    Campaign Name: {campaign_name}")
                    self.log(f"    Message Name:  {message_name}")
                    
                    # Create metadata for this specific email
                    email_metadata = base_metadata.copy()
                    email_metadata['Campaign Name'] = campaign_name
                    email_metadata['Message Name'] = message_name
                    
                    # Set current message name for warning tracking
                    extractor.current_message_name = message_name
                    
                    # Extract this email's content
                    row = extractor.prepare_row(email_info['data'], email_metadata)
                    all_rows.append(row)
                
                rows = all_rows
                
            else:
                # Original behavior: single Campaign Name for all emails
                self.log("\nNote: Document not assessed. Using single Campaign Name for all emails.")
                self.log("      (Click 'Assess Document' to assign different names per email)")
                
                # Gather user-provided metadata
                metadata = {
                    'Language': self.language_var.get().strip(),
                    'URL/UTM': self.url_var.get().strip(),
                    'End Matter (Enter Sponsor)': self.sponsor_var.get().strip()
                }
                
                # Prompt for Campaign Name if not assessed
                self.log("\nUsing default Campaign Name: 'Takeda Vitiligo WeConnect'")
                metadata['Campaign Name'] = 'Takeda Vitiligo WeConnect'
                
                # Extract email headers for logging
                self.log("\nScanning document for email headers...")
                email_headers = extractor.extract_email_headers_from_doc()
                
                if email_headers:
                    self.log(f"  Found {len(email_headers)} email template(s):")
                    for email_num, header_text in sorted(email_headers.items()):
                        # Keep full header text for message name
                        message_name = header_text  # Keep "Email 1: Long-form email"
                        self.log(f"    {email_num}. {message_name}")
                else:
                    self.log("  Warning: No email headers found")
                
                # Extract content
                self.log("\nExtracting content...")
                self.log("  [Color Detection: GREEN=Variable, RED=Standard/Skip]")
                self.log("  [Checkbox Detection: [X] marks selected options]")
                rows = extractor.extract_all_emails(metadata)
            
            self.log(f"\n[SUCCESS] Extracted {len(rows)} email template(s)")
            
            # Check for warnings
            if extractor.has_warnings():
                self.log("\n" + "!"*80)
                self.log("WARNING: Missing Checkbox Selections Detected!")
                self.log("!"*80)
                
                # Group warnings by message name
                from collections import defaultdict
                warnings_by_message = defaultdict(list)
                for warning in extractor.get_warnings():
                    message_name = warning.get('message_name', 'Unknown Email')
                    warnings_by_message[message_name].append(warning)
                
                # Display warnings grouped by message
                for message_name, warnings in sorted(warnings_by_message.items()):
                    self.log(f"\n  Email: {message_name}")
                    for warning in warnings:
                        self.log(f"     - {warning['field']}")
                        self.log(f"       > {warning['action']}")
                
                self.log("\nRecommendation: Add [X] to mark selections in Word doc, then re-extract.")
                self.log("!"*80)
            
            # Preview first row
            if rows:
                self.log("\nPreview (Row 1):")
                for col in ['Campaign Name', 'Email Subject Line', 'Banner Headline']:
                    value = rows[0].get(col, '')
                    if value:
                        preview = value[:80] + "..." if len(value) > 80 else value
                        self.log(f"  {col}: {preview}")
            
            # Export
            exporter = GoogleSheetsExporter(CampaignExtractor.STANDARD_COLUMNS)
            
            # TSV file
            output_file = Path(doc_path).stem + '_for_google_sheets.tsv'
            exporter.to_tsv(rows, output_file)
            self.log(f"\n[+] TSV file created: {output_file}")
            
            # JSON file
            import json
            json_file = Path(doc_path).stem + '_extracted.json'
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(rows, f, indent=2, ensure_ascii=False)
            self.log(f"[+] JSON file created: {json_file}")
            
            # Markdown file (with formatting preserved)
            markdown_file = Path(doc_path).stem + '_formatted.md'
            exporter.to_markdown(rows, markdown_file)
            self.log(f"[+] Markdown file created: {markdown_file}")
            
            # Handle image upload based on user selection
            if hasattr(self, 'detected_images') and self.detected_images and hasattr(self, 'image_upload_option'):
                upload_option = self.image_upload_option.get()
                
                if upload_option == "all":
                    self.log("\n" + "="*80)
                    self.log("PROCESSING IMAGES")
                    self.log("="*80)
                    
                    # Save all images locally first
                    saved_files = extractor.save_images_to_folder(self.detected_images)
                    
                    self.log(f"\nSaved {len(saved_files)} image(s) to 'campaign_images/' folder:")
                    for filepath in saved_files:
                        self.log(f"  {filepath}")
                    
                    # Check Git status before auto-upload
                    if hasattr(self, 'git_status') and self.git_status.get('errors'):
                        self.log("\n" + "="*80)
                        self.log("GIT AUTO-UPLOAD SKIPPED")
                        self.log("="*80)
                        self.log("\nImages saved locally but NOT uploaded to GitHub.")
                        self.log("Git setup issues detected during assessment:")
                        for error in self.git_status['errors']:
                            self.log(f"  • {error}")
                        self.log("\nFix Git issues and re-extract to enable auto-upload.")
                        self.log("\nManual upload: Use GitHub Desktop to commit and push")
                    else:
                        # Automatically upload to GitHub
                        campaign_name = self.dynamic_campaign_fields[0]['campaign_var'].get() if self.dynamic_campaign_fields else "campaign"
                        upload_success, image_urls = self.auto_upload_to_github(saved_files, campaign_name)
                        
                        # Update rows with GitHub image URLs
                        if upload_success and image_urls:
                            self.log("\nUpdating extracted data with GitHub image URLs...")
                            rows = self.update_rows_with_image_urls(rows, image_urls)
                            self.log("  Image URLs inserted into Hero Image (URL) column!")
                    
                elif upload_option == "select":
                    selected_images = [img for img in self.detected_images if img.get('selected', False)]
                    
                    if selected_images:
                        self.log("\n" + "="*80)
                        self.log(f"PROCESSING SELECTED IMAGES ({len(selected_images)}/{len(self.detected_images)})")
                        self.log("="*80)
                        
                        saved_files = extractor.save_images_to_folder(selected_images)
                        
                        self.log(f"\nSaved {len(saved_files)} selected image(s):")
                        for filepath in saved_files:
                            self.log(f"  {filepath}")
                        
                        # Check Git status before auto-upload
                        if hasattr(self, 'git_status') and self.git_status.get('errors'):
                            self.log("\n" + "="*80)
                            self.log("GIT AUTO-UPLOAD SKIPPED")
                            self.log("="*80)
                            self.log("\nImages saved locally but NOT uploaded to GitHub.")
                            self.log("Git setup issues detected during assessment:")
                            for error in self.git_status['errors']:
                                self.log(f"  • {error}")
                            self.log("\nFix Git issues and re-extract to enable auto-upload.")
                            self.log("\nManual upload: Use GitHub Desktop to commit and push")
                        else:
                            # Automatically upload to GitHub
                            campaign_name = self.dynamic_campaign_fields[0]['campaign_var'].get() if self.dynamic_campaign_fields else "campaign"
                            upload_success, image_urls = self.auto_upload_to_github(saved_files, campaign_name)
                            
                            # Update rows with GitHub image URLs
                            if upload_success and image_urls:
                                self.log("\nUpdating extracted data with GitHub image URLs...")
                                rows = self.update_rows_with_image_urls(rows, image_urls)
                                self.log("  Image URLs inserted into Hero Image (URL) column!")
                    else:
                        self.log("\nNo images selected for upload")
                
                else:  # skip
                    self.log("\nImage upload skipped (manual handling)")
            
            # Clipboard
            if exporter.to_clipboard(rows):
                self.log(f"\n[SUCCESS] Content copied to clipboard!")
                self.log(f"           {len(rows)} row(s) ready to paste")
            else:
                self.log("\n[Note] Could not copy to clipboard, use TSV file")
            
            self.log("\n" + "=" * 80)
            self.log("NEXT STEPS:")
            self.log("=" * 80)
            self.log("1. Open your Google Sheets campaign spreadsheet")
            self.log("2. Click on the first empty row")
            self.log("3. Press Ctrl+V to paste")
            self.log("4. Review the content")
            self.log("5. Add Hero Image URLs if needed")
            self.log("6. Check the box in Column A to generate JSON!")
            
            self.root.after(0, lambda: self.status_var.set("Extraction complete! Content copied to clipboard."))
            
            # Show warning dialog if there are missing selections
            if extractor.has_warnings():
                # Group warnings by message name
                from collections import defaultdict
                warnings_by_message = defaultdict(list)
                for warning in extractor.get_warnings():
                    message_name = warning.get('message_name', 'Unknown Email')
                    warnings_by_message[message_name].append(warning)
                
                # Build warnings list grouped by message
                warnings_lines = []
                for message_name, warnings in sorted(warnings_by_message.items()):
                    warnings_lines.append(f"\n{message_name}:")
                    for warning in warnings:
                        warnings_lines.append(f"  • {warning['field']}")
                
                warnings_list = "\n".join(warnings_lines)
                warning_msg = (
                    f"WARNING: Missing Checkbox Selections!\n\n"
                    f"These fields have multiple options but no [X] checkbox:{warnings_list}\n\n"
                    f"Action Taken: Using first option as default.\n\n"
                    f"Recommendation: Add [X] to mark your preferred options\n"
                    f"in the Word document, then extract again."
                )
                self.root.after(0, lambda: messagebox.showwarning(
                    "Missing Selections Detected",
                    warning_msg
                ))
            
            # Show success message
            self.root.after(0, lambda: messagebox.showinfo(
                "Success",
                f"Extracted {len(rows)} email(s)!\n\n"
                "Content is copied to clipboard.\n"
                "Just paste it into Google Sheets (Ctrl+V)"
            ))
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.log(f"\n[ERROR] {error_msg}")
            self.root.after(0, lambda: messagebox.showerror("Extraction Error", error_msg))
            self.root.after(0, lambda: self.status_var.set("Error during extraction"))
        
        finally:
            # Re-enable button and stop progress
            self.root.after(0, lambda: self.extract_btn.config(state="normal"))
            self.root.after(0, lambda: self.progress.stop())


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ExtractorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

