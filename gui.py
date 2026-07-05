import threading
import tkinter as tk
from tkinter import ttk, messagebox
from main import WebAutomation


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Automation Engine")

        # Center the window on the screen
        window_width = 500
        window_height = 650
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.root.resizable(False, False)

        self.web_automation = None

        # Theme config
        style = ttk.Style()
        style.theme_use("clam")

        # Color palette
        bg_color = "#0D0D0D"
        surface_color = "#1A1A1A"
        fg_color = "#F2F2F2"
        muted_fg = "#A0A0A0"
        accent_blue = "#0A84FF"
        accent_blue_hover = "#0066CC"
        accent_red = "#FF453A"
        accent_red_hover = "#D70015"

        self.root.configure(bg=bg_color)

        # Global styles
        style.configure("TFrame", background=bg_color)
        style.configure(
            "TLabel", background=bg_color, foreground=muted_fg, font=("Segoe UI", 10)
        )

        # Typography hierarchy
        style.configure(
            "Title.TLabel", foreground=fg_color, font=("Segoe UI", 22, "bold")
        )
        style.configure(
            "Subtitle.TLabel", foreground=accent_blue, font=("Segoe UI", 10)
        )

        # Input fields
        style.configure(
            "TEntry",
            fieldbackground=surface_color,
            foreground=fg_color,
            borderwidth=0,
            padding=10,
        )

        # Buttons
        style.configure(
            "Primary.TButton",
            background=accent_blue,
            foreground="white",
            font=("Segoe UI", 11, "bold"),
            padding=10,
            borderwidth=0,
        )
        style.map(
            "Primary.TButton",
            background=[("active", accent_blue_hover), ("disabled", "#333333")],
        )

        style.configure(
            "Danger.TButton",
            background=accent_red,
            foreground="white",
            font=("Segoe UI", 11, "bold"),
            padding=10,
            borderwidth=0,
        )
        style.map("Danger.TButton", background=[("active", accent_red_hover)])

        # UI layout
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(padx=40, pady=35, fill="both", expand=True)

        # Header Section
        ttk.Label(
            self.main_container, text="Automation Setup", style="Title.TLabel"
        ).pack(anchor="w")
        ttk.Label(
            self.main_container,
            text="Configure your credentials and data to start.",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(0, 30))

        # Form Container
        self.form_frame = ttk.Frame(self.main_container)
        self.form_frame.pack(fill="x")
        self.form_frame.columnconfigure(1, weight=1)

        # Helper to create perfectly aligned rows
        def add_field(row, label_text, show_char=None, pady=10):
            ttk.Label(self.form_frame, text=label_text).grid(
                row=row, column=0, sticky="w", pady=pady, padx=(0, 15)
            )
            entry = ttk.Entry(self.form_frame, font=("Segoe UI", 11), show=show_char)
            entry.grid(row=row, column=1, sticky="ew", pady=pady)
            return entry

        # Credentials Group
        self.entry_username = add_field(0, "Username", pady=(0, 8))
        self.entry_password = add_field(1, "Password", show_char="*", pady=(0, 20))

        # Subtle horizontal divider
        ttk.Separator(self.form_frame, orient="horizontal").grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=(0, 20)
        )

        # Personal Info Group
        self.entry_fullname = add_field(3, "Full Name", pady=(0, 8))
        self.entry_email = add_field(4, "Email", pady=(0, 8))
        self.entry_current_address = add_field(5, "Current Address", pady=(0, 8))
        self.entry_permanent_address = add_field(6, "Permanent Address", pady=(0, 8))

        # Buttons Container
        self.button_frame = ttk.Frame(self.main_container)
        self.button_frame.pack(fill="x", pady=(35, 0))
        # Allow buttons to take equal space horizontally
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)

        self.submit_button = ttk.Button(
            self.button_frame,
            text="Start Engine",
            style="Primary.TButton",
            command=self.start_automation_thread,
        )
        self.submit_button.grid(row=0, column=0, padx=(0, 8), sticky="ew")

        self.close_btn = ttk.Button(
            self.button_frame,
            text="Close Browser",
            style="Danger.TButton",
            command=self.close_browser,
        )
        self.close_btn.grid(row=0, column=1, padx=(8, 0), sticky="ew")

    # Functions
    def start_automation_thread(self):
        # Disable button to prevent multi-clicks
        self.submit_button.config(state=tk.DISABLED)
        thread = threading.Thread(target=self.execute_automation)
        thread.start()

    def execute_automation(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        fullname = self.entry_fullname.get()
        email = self.entry_email.get()
        current_address = self.entry_current_address.get()
        permanent_address = self.entry_permanent_address.get()

        try:
            self.web_automation = WebAutomation()
            self.web_automation.login(username, password)
            self.web_automation.fill_form(
                fullname, email, current_address, permanent_address
            )
            self.web_automation.download()

            self.root.after(
                0,
                lambda: messagebox.showinfo(
                    "Success", "Automation completed successfully!"
                ),
            )
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally:
            self.root.after(0, lambda: self.submit_button.config(state=tk.NORMAL))

    def close_browser(self):
        if self.web_automation:
            self.web_automation.close()
            self.web_automation = None
            messagebox.showinfo("Browser", "Browser closed successfully.")
        else:
            messagebox.showwarning("Warning", "No active browser session to close.")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
