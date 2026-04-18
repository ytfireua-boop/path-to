#!/usr/bin/env python3
"""
path-to - A command-line tool to find the full path to files in the current directory and subdirectories.
Includes Tkinter GUI installer functionality.
"""

import os
import sys
import argparse
import subprocess
import threading
import time
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext


def find_file(filename, search_dir="."):
    """
    Search for a file in the given directory and its subdirectories.
    
    Args:
        filename (str): Name of the file to search for
        search_dir (str): Directory to search in (default: current directory)
    
    Returns:
        list: List of found file paths
    """
    found_files = []
    search_path = Path(search_dir).resolve()
    
    try:
        # Search for exact filename matches
        for file_path in search_path.rglob(filename):
            if file_path.is_file():
                found_files.append(str(file_path))
        
        # If no exact matches, search for partial matches
        if not found_files:
            for file_path in search_path.rglob(f"*{filename}*"):
                if file_path.is_file():
                    found_files.append(str(file_path))
    
    except PermissionError:
        print(f"Error: Permission denied while searching in {search_dir}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return []
    
    return found_files


def main():
    """Main command-line interface"""
    parser = argparse.ArgumentParser(
        description="Find the full path to files in the current directory and subdirectories.",
        prog="path-to"
    )
    parser.add_argument(
        "filename",
        nargs="?",
        help="Name of the file to search for"
    )
    parser.add_argument(
        "-d", "--directory",
        default=".",
        help="Directory to search in (default: current directory)"
    )
    parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="Show all matches instead of just the first one"
    )
    parser.add_argument(
        "-c", "--count",
        action="store_true",
        help="Show only the count of matching files"
    )
    parser.add_argument(
        "--installer",
        action="store_true",
        help="Launch the GUI installer"
    )
    
    args = parser.parse_args()
    
    # Launch GUI installer if requested
    if args.installer:
        launch_installer()
        return
    
    # If no filename provided, show help
    if not args.filename:
        parser.print_help()
        return
    
    found_files = find_file(args.filename, args.directory)
    
    if args.count:
        print(len(found_files))
        return
    
    if not found_files:
        print(f"No files found matching '{args.filename}' in '{args.directory}'")
        sys.exit(1)
    
    if args.all:
        for file_path in found_files:
            print(file_path)
    else:
        print(found_files[0])


class PathToInstaller:
    def __init__(self, root):
        self.root = root
        self.root.title("path-to Installer")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Variables
        self.installation_complete = False
        self.is_installed = self.check_installation()
        self.current_operation = None
        
        self.create_widgets()
        
    def check_installation(self):
        """Check if path-to is already installed"""
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "show", "path-to"], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Title Frame
        title_frame = ttk.Frame(self.root, padding="20")
        title_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(title_frame, text="path-to Installer", 
                                font=("Arial", 16, "bold"))
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, 
                                   text="A command-line tool to find file paths",
                                   font=("Arial", 10))
        subtitle_label.pack(pady=(5, 0))
        
        # Main Content Frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status Frame
        status_frame = ttk.LabelFrame(main_frame, text="Installation Status", padding="10")
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, 
                                     text="Status: Ready to install" if not self.is_installed else "Status: Already installed",
                                     font=("Arial", 10))
        self.status_label.pack()
        
        # Progress Bar
        self.progress = ttk.Progressbar(status_frame, mode='determinate')
        self.progress.pack(fill=tk.X, pady=(10, 0))
        
        # Console Output Frame
        console_frame = ttk.LabelFrame(main_frame, text="Installation Log", padding="10")
        console_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.console_text = scrolledtext.ScrolledText(console_frame, height=10, width=70, 
                                                      wrap=tk.WORD, font=("Consolas", 9))
        self.console_text.pack(fill=tk.BOTH, expand=True)
        
        # Button Frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        # Install button (only shown when not installed)
        self.install_btn = ttk.Button(button_frame, text="Install", 
                                           command=self.install_app)
        self.install_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Uninstall button (only shown when installed)
        self.uninstall_btn = ttk.Button(button_frame, text="Uninstall", 
                                             command=self.uninstall_app)
        self.uninstall_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Test button
        self.test_btn = ttk.Button(button_frame, text="Test Functionality", 
                                      command=self.test_installation)
        self.test_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Exit button
        exit_btn = ttk.Button(button_frame, text="Exit", command=self.root.quit)
        exit_btn.pack(side=tk.RIGHT)
        
        # Info Frame
        info_frame = ttk.LabelFrame(main_frame, text="Information", padding="10")
        info_frame.pack(fill=tk.X)
        
        info_text = """path-to is a command-line tool that helps you find the full path to files.
After installation, you can use it from any directory by typing:
  path-to <filename>

Features:
• Searches recursively through subdirectories
• Returns full absolute paths
• Supports partial filename matching
• Cross-platform compatibility"""
        
        info_label = ttk.Label(info_frame, text=info_text, font=("Arial", 9))
        info_label.pack()
        
        # Update button visibility
        self.update_button_visibility()
    
    def update_button_visibility(self):
        """Update button visibility based on installation state"""
        if self.is_installed:
            self.install_btn.pack_forget()
            self.uninstall_btn.pack(side=tk.LEFT, padx=(0, 10))
            self.test_btn.config(state=tk.NORMAL)
            self.status_label.config(text="Status: path-to is installed")
            self.status_label.config(foreground="green")
        else:
            self.uninstall_btn.pack_forget()
            self.install_btn.pack(side=tk.LEFT, padx=(0, 10))
            self.test_btn.config(state=tk.DISABLED)
            self.status_label.config(text="Status: path-to is not installed")
            self.status_label.config(foreground="red")
    
    def log_message(self, message):
        """Add message to console output"""
        timestamp = time.strftime("%H:%M:%S")
        self.console_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.console_text.see(tk.END)
        self.root.update_idletasks()
    
    def install_app(self):
        """Install the path-to application"""
        if self.current_operation:
            return
        
        if self.is_installed:
            messagebox.showinfo("Already Installed", "path-to is already installed!")
            return
        
        # Disable buttons during installation
        self.install_btn.config(state=tk.DISABLED)
        self.test_btn.config(state=tk.DISABLED)
        
        # Start installation in separate thread
        threading.Thread(target=self._install_thread, daemon=True).start()
    
    def _install_thread(self):
        """Installation thread"""
        try:
            self.current_operation = "install"
            self.log_message("Starting installation...")
            self.progress.config(mode='indeterminate')
            self.progress.start()
            self.status_label.config(text="Status: Installing...")
            
            # Get current directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.log_message(f"Installing from: {current_dir}")
            
            # Install using pip
            self.log_message("Running pip install...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", current_dir], 
                                  capture_output=True, text=True)
            
            self.progress.stop()
            self.progress.config(mode='determinate')
            self.progress.config(value=100)
            
            if result.returncode == 0:
                self.log_message("Installation completed successfully!")
                self.log_message("Output: " + result.stdout)
                self.installation_complete = True
                self.is_installed = True
                
                # Update UI in main thread
                self.root.after(0, self._installation_success)
            else:
                self.log_message("Installation failed!")
                self.log_message("Error: " + result.stderr)
                self.root.after(0, self._installation_failed)
                
        except Exception as e:
            self.log_message(f"Installation error: {str(e)}")
            self.progress.stop()
            self.progress.config(mode='determinate')
            self.root.after(0, self._installation_failed)
    
    def _installation_success(self):
        """Handle successful installation"""
        self.status_label.config(text="Status: Installation complete!")
        self.current_operation = None
        self.update_button_visibility()
        messagebox.showinfo("Success", "path-to has been installed successfully!")
    
    def _installation_failed(self):
        """Handle failed installation"""
        self.status_label.config(text="Status: Installation failed!")
        self.current_operation = None
        self.install_btn.config(state=tk.NORMAL)
        messagebox.showerror("Installation Failed", 
                           "Installation failed. Please check the log for details.")
    
    def uninstall_app(self):
        """Uninstall the path-to application"""
        if self.current_operation:
            return
        
        if not self.is_installed:
            messagebox.showinfo("Not Installed", "path-to is not installed!")
            return
        
        if messagebox.askyesno("Confirm Uninstall", 
                              "Are you sure you want to uninstall path-to?"):
            # Disable buttons during uninstallation
            self.uninstall_btn.config(state=tk.DISABLED)
            self.test_btn.config(state=tk.DISABLED)
            
            # Start uninstallation in separate thread
            threading.Thread(target=self._uninstall_thread, daemon=True).start()
    
    def _uninstall_thread(self):
        """Uninstallation thread"""
        try:
            self.current_operation = "uninstall"
            self.log_message("Starting uninstallation...")
            self.progress.config(mode='indeterminate')
            self.progress.start()
            self.status_label.config(text="Status: Uninstalling...")
            
            # Uninstall using pip
            self.log_message("Running pip uninstall...")
            result = subprocess.run([sys.executable, "-m", "pip", "uninstall", "path-to", "-y"], 
                                  capture_output=True, text=True)
            
            self.progress.stop()
            self.progress.config(mode='determinate')
            self.progress.config(value=100)
            
            if result.returncode == 0:
                self.log_message("Uninstallation completed successfully!")
                self.is_installed = False
                
                # Update UI in main thread
                self.root.after(0, self._uninstallation_success)
            else:
                self.log_message("Uninstallation failed!")
                self.log_message("Error: " + result.stderr)
                self.root.after(0, self._uninstallation_failed)
                
        except Exception as e:
            self.log_message(f"Uninstallation error: {str(e)}")
            self.progress.stop()
            self.progress.config(mode='determinate')
            self.root.after(0, self._uninstallation_failed)
    
    def _uninstallation_success(self):
        """Handle successful uninstallation"""
        self.status_label.config(text="Status: Uninstallation complete!")
        self.current_operation = None
        self.update_button_visibility()
        messagebox.showinfo("Success", "path-to has been uninstalled successfully!")
    
    def _uninstallation_failed(self):
        """Handle failed uninstallation"""
        self.status_label.config(text="Status: Uninstallation failed!")
        self.current_operation = None
        self.uninstall_btn.config(state=tk.NORMAL)
        messagebox.showerror("Uninstallation Failed", 
                           "Uninstallation failed. Please check the log for details.")
    
    def test_installation(self):
        """Test the installation"""
        if self.current_operation:
            return
        
        if not self.is_installed:
            messagebox.showinfo("Not Installed", "path-to is not installed!")
            return
        
        # Disable buttons during test
        self.test_btn.config(state=tk.DISABLED)
        
        # Start test in separate thread
        threading.Thread(target=self._test_thread, daemon=True).start()
    
    def _test_thread(self):
        """Test thread"""
        try:
            self.current_operation = "test"
            self.log_message("Testing installation...")
            self.progress.config(mode='indeterminate')
            self.progress.start()
            self.status_label.config(text="Status: Testing...")
            
            # Test path-to command
            result = subprocess.run(["path-to", "--help"], 
                                  capture_output=True, text=True, timeout=10)
            
            self.progress.stop()
            self.progress.config(mode='determinate')
            self.progress.config(value=100)
            
            if result.returncode == 0:
                self.log_message("Test successful! path-to is working correctly.")
                self.root.after(0, self._test_success)
            else:
                self.log_message("Test failed: " + result.stderr)
                self.root.after(0, self._test_failed)
                
        except subprocess.TimeoutExpired:
            self.log_message("Test timed out!")
            self.progress.stop()
            self.progress.config(mode='determinate')
            self.root.after(0, self._test_failed)
        except Exception as e:
            self.log_message(f"Test error: {str(e)}")
            self.progress.stop()
            self.progress.config(mode='determinate')
            self.root.after(0, self._test_failed)
    
    def _test_success(self):
        """Handle successful test"""
        self.status_label.config(text="Status: Test completed successfully!")
        self.current_operation = None
        self.test_btn.config(state=tk.NORMAL)
        messagebox.showinfo("Test Successful", 
                         "path-to is working correctly!\n\nTry running 'path-to <filename>' in your command line.")
    
    def _test_failed(self):
        """Handle failed test"""
        self.status_label.config(text="Status: Test failed!")
        self.current_operation = None
        self.test_btn.config(state=tk.NORMAL)
        messagebox.showerror("Test Failed", 
                           "Test failed. Please check the log for details.")


def launch_installer():
    """Launch the GUI installer"""
    root = tk.Tk()
    app = PathToInstaller(root)
    root.mainloop()


if __name__ == "__main__":
    main()
