import sys
import subprocess
import os
import json
import logging
import threading
import shutil
import tkinter as tk
import webbrowser
from tkinter import messagebox, scrolledtext

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class SetupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Claude Custom MCP Installer")
        self.root.geometry("600x550")
        self.root.configure(bg="#f0f0f0")
        
        # Styles
        title_font = ("Segoe UI", 18, "bold")
        desc_font = ("Segoe UI", 10)
        label_font = ("Segoe UI", 10, "bold")
        
        # Header Frame
        header = tk.Frame(root, bg="white", pady=10)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="Claude Custom MCP", font=title_font, bg="white", fg="#d9534f").pack()
        tk.Label(header, text="Installs various tools related to Cyber Sec, Obsidian, and System Control", font=desc_font, bg="white", fg="#555").pack()

        # Main Content Frame
        content = tk.Frame(root, padx=20, pady=10, bg="#f0f0f0")
        content.pack(fill=tk.BOTH, expand=True)

        # Obsidian API Key Input
        tk.Label(content, text="Obsidian Setup (Optional)", font=label_font, bg="#f0f0f0").pack(anchor="w", pady=(10, 5))
        
        key_frame = tk.Frame(content, bg="#f0f0f0")
        key_frame.pack(fill=tk.X)
        
        tk.Label(key_frame, text="Local REST API Key:", bg="#f0f0f0").pack(side=tk.LEFT)
        self.api_key_entry = tk.Entry(key_frame, width=40, show="*")
        self.api_key_entry.pack(side=tk.LEFT, padx=10)
        
        help_btn = tk.Button(key_frame, text="?", width=3, command=self.show_obsidian_help)
        help_btn.pack(side=tk.LEFT)
        
        tk.Label(content, text="Leave blank to skip Obsidian integration.", font=("Segoe UI", 8, "italic"), fg="#777", bg="#f0f0f0").pack(anchor="w")

        # Install Button
        self.install_btn = tk.Button(content, text="Install Now", font=("Segoe UI", 12, "bold"), command=self.start_install, bg="#0078D7", fg="white", padx=20, pady=8, bd=0, cursor="hand2")
        self.install_btn.pack(pady=20)
        
        # Log Area
        tk.Label(content, text="Installation Log:", bg="#f0f0f0", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.log_area = scrolledtext.ScrolledText(content, height=12, font=("Consolas", 9), relief=tk.FLAT)
        self.log_area.pack(fill=tk.BOTH, expand=True)
        
        # Determine destination for servers
        self.install_dir = os.path.join(os.path.expanduser("~"), ".mcp_servers")
        self.obsidian_key = None

    def log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        # Update GUI immediately
        self.root.update_idletasks()
        
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def show_obsidian_help(self):
        msg = ("To get this key:\n"
               "1. Open Obsidian -> Settings.\n"
               "2. Install 'Local REST API' plugin.\n"
               "3. Copy key from plugin settings.\n\n"
               "If skipped, Obsidian tools won't be configured.")
        messagebox.showinfo("Obsidian Help", msg)

    def start_install(self):
        self.obsidian_key = self.api_key_entry.get().strip()
        self.install_btn.config(state=tk.DISABLED, text="Installing...", bg="#cccccc")
        threading.Thread(target=self.run_setup, daemon=True).start()

    def run_setup(self):
        self.log("Starting setup...")
        self.log("-----------------------------------------")
        
        # 0. Check/Install Python
        if not self.check_python():
            return
        
        # 1. Install Packages (Dependencies)
        if not self.install_packages():
            self.fail_setup("Package installation failed.")
            return

        self.log("-----------------------------------------")
        
        # 2. Extract Servers (Self-Extracting logic)
        if not self.extract_servers():
            self.fail_setup("Server extraction failed.")
            return

        # 2a. Set Environment Variable for Obsidian if provided
        if self.obsidian_key:
            self.log("Setting OBSIDIAN_API_KEY environment variable...")
            # We can't easily set global env vars for Windows from python reliably without admin/restart.
            # INSTEAD: We will write it to a .env file in the obsidian server directory!
            # Or pass it in the config (not supported by current server code usually reading os.getenv)
            # Strategy: Write a .env file to the installation folder.
            try:
                env_path = os.path.join(self.install_dir, "obsidian-mcp", ".env")
                with open(env_path, "w") as f:
                    f.write(f"OBSIDIAN_API_KEY={self.obsidian_key}\n")
                self.log(f"Saved API key to {env_path}")
            except Exception as e:
                self.log(f"Failed to save API key: {e}")
        
        self.log("-----------------------------------------")
        
        # 3. Configure Claude
        if not self.create_claude_config():
            self.fail_setup("Claude config creation failed.")
            return

        self.log("-----------------------------------------")
        self.log("SUCCESS: Setup Complete!")
        messagebox.showinfo("Success", "Installation Complete!")
        
        # 4. Open Readme
        self.open_readme()
        
        self.install_btn.config(state=tk.NORMAL, text="Re-Install", bg="#0078D7")

    def fail_setup(self, reason):
        self.log(f"ERROR: {reason}")
        messagebox.showerror("Error", f"Setup Failed: {reason}")
        self.install_btn.config(state=tk.NORMAL, text="Retry Install", bg="#d9534f")

    def open_readme(self):
        """extracts and opens the readme html"""
        try:
            readme_src = self.resource_path("README.html")
            readme_dst = os.path.join(self.install_dir, "README.html")
            
            if os.path.exists(readme_src):
                shutil.copy(readme_src, readme_dst)
                self.log("Opening Documentation...")
                webbrowser.open(f"file://{readme_dst}")
            else:
                self.log("README.html not found in bundle.")
        except Exception as e:
            self.log(f"Could not open Readme: {e}")

    # --- Reused Logic from Previous Step ---
    def check_python(self):
        self.log("Checking for Python...")
        python_path = shutil.which("python")
        if python_path:
            self.log(f"Python found: {python_path}")
            return True
        self.log("Python NOT found.")
        if messagebox.askyesno("Python Missing", "Python is required. Install via Winget?"):
            return self.install_python()
        self.fail_setup("Python required.")
        return False

    def install_python(self):
        self.log("Installing Python 3.11 via Winget...")
        try:
            cmd = ["winget", "install", "-e", "--id", "Python.Python.3.11", "--accept-package-agreements", "--accept-source-agreements"]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            while True:
                out = process.stdout.readline()
                if out == '' and process.poll() is not None: break
                if out: self.log(out.strip())
            
            if process.poll() == 0:
                self.log("Python installed. Please RESTART this installer.")
                messagebox.showinfo("Restart", "Python installed. Please restart this installer.")
                self.root.destroy() 
                return False
            self.fail_setup("Winget install failed.")
            return False
        except Exception as e:
            self.fail_setup(f"Winget error: {e}")
            return False

    def install_packages(self):
        self.log("Installing packages...")
        req_file = self.resource_path("requirements.txt")
        if not os.path.exists(req_file): 
            # Fallback to local
            req_file = "requirements.txt"
            
        if not os.path.exists(req_file):
            self.log("requirements.txt not found.")
            return False
            
        try:
            cmd = ["python", "-m", "pip", "install", "-r", req_file, "--disable-pip-version-check"]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            while True:
                out = process.stdout.readline()
                if out == '' and process.poll() is not None: break
                if out: self.log(out.strip())
            return process.poll() == 0
        except Exception as e:
            self.log(f"Pip error: {e}")
            return False

    def extract_servers(self):
        self.log("Extracting servers...")
        servers = ["obsidian-mcp", "wifi-nmap-mcp", "system-mcp"]
        try:
            if not os.path.exists(self.install_dir): os.makedirs(self.install_dir)
            for s in servers:
                src = self.resource_path(s)
                dst = os.path.join(self.install_dir, s)
                
                # Check if we intended to bundle but it's missing (dev mode)
                if not os.path.exists(src):
                     src = os.path.abspath(s) # Check CWD

                if os.path.exists(src):
                    self.log(f"Copying {s}...")
                    if os.path.exists(dst): shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                else:
                    self.log(f"WARNING: Source for {s} not found.")
            return True
        except Exception as e:
            self.log(f"Extraction error: {e}")
            return False

    def create_claude_config(self):
        self.log("Configuring Claude...")
        appdata = os.getenv('APPDATA')
        if not appdata: return False
        
        config_path = os.path.join(appdata, "Claude", "claude_desktop_config.json")
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        python_exe = shutil.which("python") or "python"
        
        servers = {}
        
        # Add WiFi/Nmap
        servers["wifi-nmap"] = {
            "command": python_exe,
            "args": [os.path.join(self.install_dir, "wifi-nmap-mcp", "wifi_nmap_server.py")]
        }
        
        # Add System
        servers["system"] = {
            "command": python_exe,
            "args": [os.path.join(self.install_dir, "system-mcp", "system_server.py")]
        }
        
        # Add Obsidian ONLY if key provided
        if self.obsidian_key:
            servers["obsidian"] = {
                "command": python_exe,
                "args": [os.path.join(self.install_dir, "obsidian-mcp", "obsidian_server.py")]
            }
        else:
            self.log("Skipping Obsidian configuration (No API Key provided).")

        config_data = { "mcpServers": servers }
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2)
            self.log(f"Config saved.")
            return True
        except Exception as e:
            self.log(f"Config error: {e}")
            return False

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = SetupApp(root)
        root.mainloop()
    except Exception as e:
        with open("setup_crash.log", "w") as f:
            f.write(str(e))
