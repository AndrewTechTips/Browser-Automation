<div align="center">

  <h1>🤖 Web Automation Engine</h1>

  <p>
    A desktop automation tool that drives a real browser through a <strong>Tkinter GUI</strong>.<br />
    Enter your credentials and data, click <em>Start Engine</em> — <strong>Selenium</strong> handles the rest:
    login, form fill, and file download, all without touching the browser manually.
  </p>

  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white" alt="Selenium" />
    <img src="https://img.shields.io/badge/Tkinter-GUI-orange?style=for-the-badge" alt="Tkinter" />
    <img src="https://img.shields.io/badge/Threading-✓-blue?style=for-the-badge" alt="Threading" />
    <img src="https://img.shields.io/badge/Chrome-WebDriver-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Chrome" />
  </p>

</div>

<br />

---

## ✨ Features

* **🖥️ Desktop GUI:** Clean dark Tkinter interface with credential and personal info fields — no terminal interaction needed.
* **🔐 Automated Login:** Selenium fills and submits the login form, then waits for the URL to change before proceeding.
* **📝 Form Automation:** Navigates the site structure, locates the text box form, and fills all fields automatically.
* **📥 Auto Download:** Navigates to the Upload & Download section and triggers the file download directly via JavaScript click.
* **🧵 Background Threading:** Automation runs on a separate thread — the GUI never freezes during execution.
* **⚠️ Error Handling:** `TimeoutException` is caught at every step and surfaced as a readable error popup in the GUI.

---

## 🧠 Under the Hood

### Clean Separation of Concerns
The project is split into two files — `gui.py` handles all Tkinter UI logic, `main.py` contains the `WebAutomation` class. The GUI simply calls three methods in sequence:

```python
self.web_automation = WebAutomation()
self.web_automation.login(username, password)
self.web_automation.fill_form(fullname, email, current_address, permanent_address)
self.web_automation.download()
```

### Non-Blocking Execution
The automation runs on a daemon thread so the Tkinter main loop stays responsive. GUI updates (button state, popups) are safely scheduled back on the main thread with `root.after()`:

```python
thread = threading.Thread(target=self.execute_automation)
thread.start()

# Safe GUI update from background thread
self.root.after(0, lambda: messagebox.showinfo("Success", "Automation completed!"))
```

### WebDriverWait Over time.sleep()
Every element interaction uses explicit waits instead of arbitrary sleeps — the script proceeds only when elements are actually visible and ready:

```python
self.wait = WebDriverWait(self.driver, 10)

username_field = self.wait.until(
    EC.visibility_of_element_located((By.ID, "userName"))
)
```

---

## 📁 Project Structure

```
Web-Automation-Engine/
├── gui.py          # Tkinter GUI — layout, styling, threading
├── main.py         # WebAutomation class — login, form fill, download
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

1. **Clone the repository:**
    ```bash
    git clone https://github.com/AndrewTechTips/Web-Automation-Engine.git
    cd Web-Automation-Engine
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Make sure ChromeDriver is available:**
    Selenium 4 manages ChromeDriver automatically — as long as Google Chrome is installed, no manual setup is needed.

4. **Run the app:**
    ```bash
    python gui.py
    ```

---

## 📬 Contact

* **LinkedIn:** [Andrei Condrea](https://www.linkedin.com/in/andrei-condrea-b32148346)
* **Email:** condrea.andrey777@gmail.com

<p align="center">
  <i>"Why click manually when the machine can do it for you?" ⚡</i>
</p>