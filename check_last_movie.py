import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Global variable to store the last movie name


def get_last_nkiri_movie_name():
    global last_nkiri_movie_name

    # Configure Chrome options for the website
    brave_path = "FROM-NKIRI\MOVIES\Chrome\Application\chrome.exe"
    options = Options()
    options.binary_location = brave_path
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Define the URL of the webpage to open
        flexcinemaz_url = "https://flexcinemaz.com/user/login"
        driver.get(flexcinemaz_url)

        # Login process
        input_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div/div[1]/div/div[2]/form/input[1]')
        input_element.clear()
        input_element.send_keys("benjamin@flexcinemaz.com")

        input_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div/div[1]/div/div[2]/form/input[2]')
        input_element.clear()
        input_element.send_keys("benjamin@")

        wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
        next_button = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div/div[1]/div/div[2]/form/div[3]/button')))
        next_button.click()

        # Define the base URL of the webpage to scrape movie data
        url = "https://flexcinemaz.com/admin/videos/"
        driver.get(url)

        # Locate the first movie name element using XPath
        movie_name_element = driver.find_element(By.XPATH, "/html/body/main/div[2]/table/tbody/tr[1]/td[4]/a/strong")

        # Extract the text of the movie name element
        last_nkiri_movie_name = movie_name_element.text
        
        print(f"First movie name: {last_nkiri_movie_name}")
        return last_nkiri_movie_name

    finally:
        # Close the WebDriver
        driver.quit()

