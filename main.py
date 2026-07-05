import time
import os

from selenium import webdriver
from selenium.common import WebDriverException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebAutomation:
    def __init__(self):
        # Define driver, options and service
        chrome_options = Options()

        # Disable search engine choice (if appears)
        chrome_options.add_argument("--disable-search-engine-choice-screen")

        prefs = {"download.default_directory": os.getcwd()}
        chrome_options.add_experimental_option("prefs", prefs)

        try:
            self.driver = webdriver.Chrome(options=chrome_options)

            # Define a global wait
            self.wait = WebDriverWait(self.driver, 10)
        except WebDriverException as e:
            raise Exception(f"Failed to initialize the browser: {e}")

    def login(self, username, password):
        try:
            # Load the webpage
            self.driver.get("https://demoqa.com/login")

            # Locate username, password, and the login button
            username_field = self.wait.until(
                EC.visibility_of_element_located((By.ID, "userName"))
            )
            password_field = self.wait.until(
                EC.visibility_of_element_located((By.ID, "password"))
            )
            login_button = self.driver.find_element(By.ID, "login")

            # Fill in username and password and click the button
            username_field.send_keys(username)
            password_field.send_keys(password)
            self.driver.execute_script("arguments[0].click();", login_button)

            # Wait until the login is done, then execute the rest of the script
            self.wait.until(EC.url_changes("https://demoqa.com/login"))
        except TimeoutException:
            raise Exception(
                "Login failed: The elements took too long to load or credentials are wrong."
            )

    def fill_form(self, fullname, email, current_address, permanent_address):
        try:
            # Locate the Elements dropdown and Text Box
            elements = self.wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="root"]/div/div/div/div[1]/div/div/div[1]/span/div',
                    )
                )
            )
            elements.click()

            text_box = self.wait.until(
                EC.visibility_of_element_located((By.ID, "item-0"))
            )
            text_box.click()

            # Locate the form fields and submit button
            fullname_field = self.wait.until(
                EC.visibility_of_element_located((By.ID, "userName"))
            )
            email_field = self.wait.until(
                EC.visibility_of_element_located((By.ID, "userEmail"))
            )
            current_address_field = self.wait.until(
                EC.visibility_of_element_located((By.ID, "currentAddress"))
            )
            permanent_address_field = self.wait.until(
                EC.visibility_of_element_located((By.ID, "permanentAddress"))
            )
            submit_button = self.driver.find_element(By.ID, "submit")

            # Fill in the form fields
            fullname_field.send_keys(fullname)
            email_field.send_keys(email)
            current_address_field.send_keys(current_address)
            permanent_address_field.send_keys(permanent_address)

            self.driver.execute_script("arguments[0].click();", submit_button)
        except TimeoutException:
            raise Exception(
                "Form submission failed: Could not locate one or more fields."
            )

    def download(self):
        try:
            # Locate the Upload and Download section and the Download button
            upload_download = self.wait.until(
                EC.element_to_be_clickable((By.ID, "item-7"))
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", upload_download
            )
            time.sleep(1)
            upload_download.click()

            download_button = self.driver.find_element(By.ID, "downloadButton")
            self.driver.execute_script("arguments[0].click();", download_button)
        except TimeoutException:
            raise Exception(
                "Download failed: Could not interact with the download elements."
            )

    def close(self):
        if hasattr(self, "driver"):
            self.driver.quit()


if __name__ == "__main__":
    try:
        bot = WebAutomation()
        bot.login("python_student", "PYTHON_student123@")
        bot.fill_form("John Smith", "john@gmail.com", "Street 1", "Street 2")
        bot.download()
    except Exception as error:
        print(f"Error occurred: {error}")
    finally:
        bot.close()
