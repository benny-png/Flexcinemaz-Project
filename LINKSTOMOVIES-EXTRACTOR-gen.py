import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
#from check_last_movie import get_last_nkiri_movie_name
import sys
import os

import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# first get last movie_name from python file imported from check_last_movie import get_last_nkiri_movie_name
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def get_last_nkiri_movie_name():
    global last_nkiri_movie_name

    # Configure Chrome options for the website
    brave_path = resource_path("FROM-NKIRI\MOVIES\Chrome\Application\chrome.exe")
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



global last_nkiri_movie_name

last_nkiri_movie_name = get_last_nkiri_movie_name()





# Configure Chrome options for the website
brave_path = resource_path("FROM-NKIRI\MOVIES\Chrome\Application\chrome.exe")
options = Options()
options.binary_location = brave_path
#options.add_argument("user-data-dir=D:\selenium")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')


# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Define the base URL of the webpage to scrape movie data
base_url = "https://nkiri.com/category/international"

# Function to extract and save movie data to a CSV file
def extract_and_save_movie_data():
    page_number = 1
    movie_data = []  # Use a list to preserve order

    
    
    while page_number < 10 :  # Scrape up to 10 pages
        page_url = base_url if page_number == 1 else f"{base_url}/page/{page_number}/"
        driver.get(page_url)

        # Find all 'a' elements with the specified attributes
        movie_elements = driver.find_elements(By.XPATH, '//a[@rel="bookmark"]')

        for element in movie_elements:
            title = element.text

            link = element.get_attribute('href')
            
            # Extract the year from the title
            year = title.split(" | ")[0].split(" (")[-1].rstrip(")")
            title = title.split(" (")[0]
            
            if title == last_nkiri_movie_name :
                page_number = 10
                break
            movie_data.append({"MOVIE_TITLE": title, "YEAR": year, "LINK": link})
            print(title)
        # Print progress
        print(f"Page {page_number} scraped.")
        
        page_number += 1
        
    # Reverse the order of the movie data to get last movie as first ID movie in flexcinemaz 
    movie_data.reverse()
        
    # Save the movie data in a CSV file
    csv_filename = "NETNAIJAORGANIZEDMOVIES1.csv"
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ["MOVIE_TITLE", "YEAR", "LINK"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(movie_data)

    print(f"Movie data extracted and saved to {csv_filename}")
    
    try:
        # Save the last movie to a text file
        last_movie_title = movie_data[0]["MOVIE_TITLE"]
        with open("last_movie.txt", 'w') as txtfile:
            txtfile.write(last_movie_title)

        print(f"Last movie title saved to last_movie.txt")
    except:
        pass


# Call the function to extract and save movie data
extract_and_save_movie_data()

# Close the WebDriver
driver.quit()



import re
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Configure Chrome options for the website
brave_path = resource_path("FROM-NKIRI\MOVIES\Chrome\Application\chrome.exe")
options = Options()
options.binary_location = brave_path
#options.add_argument("user-data-dir=D:\selenium")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')


# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Initialize an empty list to store the movie data
movie_data = []

def extract_movie_data(movie_url):
    seen_movie_links = set()
    # Open the URL
    driver.get(movie_url)
    
    while True:
        movie_elements = driver.find_elements(By.CSS_SELECTOR, "a[href^='https://wetafiles.com/'], a[href^='https://downloadwella.com/']")
        
        if not movie_elements:
            break  # Exit the loop if no more elements are found
        
        for element in movie_elements:
            href = element.get_attribute("href")
            if href in seen_movie_links:
                return  # Exit the function if you encounter a repeated movie link
            
            # Extract the movie title and year from the link
            
            title = row['MOVIE_TITLE']  # Replace dots with spaces
            year = row['YEAR']
       
            seen_movie_links.add(href)
            movie_data.append({"MOVIE_TITLE": title, "YEAR": year, "LINK": href})
            print(f"Scraped: {title} {year} - {href}")

# Modify your code to pass the movie URL to the function
with open('NETNAIJAORGANIZEDMOVIES1.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        link = row["LINK"]
        print(f"Scraping: {link}")
        extract_movie_data(link)
        print(f"Finished scraping: {link}")

# Define the CSV filename to save the data
csv_filename = "NETNAIJAORGANIZEDMOVIES.csv"

# Write the extracted movie data to a CSV file
with open(csv_filename, "w", newline="") as csvfile:
    fieldnames = ["MOVIE_TITLE", "YEAR", "LINK"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(movie_data)

# Close the WebDriver
driver.quit()

print(f"Scraped {len(movie_data)} unique movie records and saved to {csv_filename}.")



import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Configure Chrome options for the website
brave_path = resource_path("FROM-NKIRI\MOVIES\Chrome\Application\chrome.exe")
options = Options()
options.binary_location = brave_path
#options.add_argument("user-data-dir=D:\selenium")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Define the URL of the webpage to search for movies by title
search_url = "https://www.themoviedb.org/search?query="

# Open the CSV file for reading
with open('NETNAIJAORGANIZEDMOVIES.csv', 'r') as csvfile:
    csv_reader = csv.reader(csvfile)
    header = next(csv_reader)  # Skip the header row

    # Initialize movie_data list
    movie_data = []
    seen_titles = set()  # Keep track of seen movie titles

    # Iterate through the rows in the CSV
    for row in csv_reader:
        movie_title, year, movie_url = row

        # Check if the movie title has already been seen
        if movie_title in seen_titles:
            print(f"Duplicate movie title found: '{movie_title}', skipping...")
            continue

        # Function to search for movie data and extract movie IDs with a year filter
        def search_and_extract_movie_id():
            search_query = movie_title.replace(' ', '%20')
            search_query_url = f"{search_url}{search_query} y:{year}"

            # Open the search URL
            driver.get(search_query_url)

            try:
                # Parse the page with BeautifulSoup
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Find the div with class "search_results movie"
                results_div = soup.find('div', class_='search_results movie')

                if results_div:
                    # Find the first anchor element containing "/movie/" in its href
                    first_result = results_div.find('a', href=lambda href: href and '/movie/' in href)

                    if first_result:
                        # Extract the movie ID from the 'href' attribute
                        movie_id = first_result['href'].split("/movie/")[1]
                        return movie_id

                return None
            except:
                return None

        movie_id = search_and_extract_movie_id()
        if movie_id:
            seen_titles.add(movie_title)  # Add movie title to the set
            movie_data.append({
                "MOVIE_TITLE": movie_title,
                "YEAR": year,
                "MOVIE_LINK": movie_url,
                "MOVIE_ID": movie_id
            })
            print(f"Scraped Movie ID for '{movie_title}': {movie_id}")

# Define the new CSV filename to save the data
csv_filename = "NETNAIJAORGANIZEDMOVIES_WITH_IDS.csv"

# Write the extracted movie data to a new CSV file
with open(csv_filename, "w", newline="") as csvfile:
    fieldnames = ["MOVIE_TITLE", "YEAR", "MOVIE_LINK", "MOVIE_ID"]
    csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    csv_writer.writeheader()
    csv_writer.writerows(movie_data)

# Close the WebDriver
driver.quit()

print(f"Scraped {len(movie_data)} movie records and saved to {csv_filename}.")




import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Configure Chrome options for the website
brave_path = resource_path("FROM-NKIRI\MOVIES\Chrome\Application\chrome.exe")
options = Options()
options.binary_location = brave_path
#options.add_argument("user-data-dir=D:\selenium")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the CSV file for reading
with open('NETNAIJAORGANIZEDMOVIES_WITH_IDS.csv', 'r') as csvfile:
    csv_reader = csv.reader(csvfile)
    header = next(csv_reader)  # Skip the header row

    # Initialize movie_data list
    movie_data = []

    # Iterate through the rows in the CSV
    for row in csv_reader:
        movie_title, year, movie_link, movie_id = row

        # Function to scrape YouTube trailer data and add to movie_data
        def scrape_youtube_trailer():
            youtube_url = "https://www.themoviedb.org/movie/" + movie_id
            driver.get(youtube_url)
            time.sleep(2)  # Add a delay to ensure the page loads properly

            try:
                # Parse the page with BeautifulSoup
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Find the first anchor element with the class "play_trailer"
                trailer_element = soup.find('a', class_='no_click play_trailer')

                # Extract the data-id attribute (YouTube trailer ID)
                youtube_id = trailer_element['data-id']
                return youtube_id
            except:
                return None

        youtube_id = scrape_youtube_trailer()
        if youtube_id:
            movie_data.append({
                "MOVIE_TITLE": movie_title,
                "YEAR": year,
                "MOVIE_LINK": movie_link,
                "MOVIE_ID": movie_id,
                "YOUTUBE_URL": f"https://www.youtube.com/watch?v={youtube_id}"
            })
            print(f"Scraped YouTube ID for '{movie_title}': {youtube_id}")

# Define the new CSV filename to save the data
csv_filename = "NETNAIJAORGANIZEDMOVIES_WITH_TRAILERS.csv"

# Write the extracted movie data with YouTube trailers to a new CSV file
with open(csv_filename, "w", newline="") as csvfile:
    fieldnames = ["MOVIE_TITLE", "YEAR", "MOVIE_LINK", "MOVIE_ID", "YOUTUBE_URL"]
    csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    csv_writer.writeheader()
    csv_writer.writerows(movie_data)

# Close the WebDriver
driver.quit()

print(f"Scraped YouTube trailer data for {len(movie_data)} movies and saved to {csv_filename}.")



import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Configure Chrome options for the website
brave_path = resource_path("FROM-NKIRI\MOVIES\Chrome\Application\chrome.exe")
options = Options()
options.binary_location = brave_path
#options.add_argument("user-data-dir=D:\selenium")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()

# Define the URL of the webpage to open
flexcinemaz_url = "https://flexcinemaz.com/user/login"

driver.get('https://flexcinemaz.com/user/login')

input_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div/div[1]/div/div[2]/form/input[1]')
# Write "Server 1" to the input element
input_element.clear()  # Clear any existing text
input_element.send_keys("benjamin@flexcinemaz.com")

input_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div/div[1]/div/div[2]/form/input[2]')
# Write "Server 1" to the input element
input_element.clear()  # Clear any existing text
input_element.send_keys("benjamin@")


wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
next_button = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div/div[1]/div/div[2]/form/div[3]/button')))
next_button.click()

driver.get('https://flexcinemaz.com/admin/videos_add/')

#driver.get('https://flexcinemaz.com/admin/videos_add/')

# Open the CSV file for reading
with open('NETNAIJAORGANIZEDMOVIES_WITH_TRAILERS.csv', 'r') as csvfile:
    csv_reader = csv.DictReader(csvfile)

    # Iterate through the rows in the CSV
    #driver.get(flexcinemaz_url)
    i = 0
    for row in csv_reader:
        movie_id = row['MOVIE_ID']
        

        # Open the URL
        if i == 0:
           pass
           #input("Log in manually, then press Enter to continue...")

        # Find and populate the 'imdb_id' input field
        imdb_id_input = driver.find_element(By.ID,"imdb_id")
        imdb_id_input.clear()
        imdb_id_input.send_keys(movie_id)

        # Find and click the 'FETCH' button
        fetch_button = driver.find_element(By.ID,"import_btn")
        fetch_button.click()

        # Wait for a moment to allow the page to load
        time.sleep(3) # You can adjust the waiting time as needed


        checkbox = driver.find_element(By.XPATH, '//div[@class="toggle"]/label[input[@type="checkbox" and @name="enable_download"]]')
        if not checkbox.is_selected():
                # If it's not checked, check it
                checkbox.click()

        time.sleep(5)
        create_button = driver.find_element(By.XPATH, '/html/body/main/form/div/div[2]/div/div[2]/div[9]/div/button')
        driver.execute_script("arguments[0].click();", create_button)


        try: #check if the rows MOVIE ID BRINGS ERRORS IN THE 'THIS REQUIRED FIELD'
           wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
           next_button = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[4]/div/div[4]/div/button')))
           next_button.click()
        except:
            continue

        input_element = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[2]/div[1]/div[1]/div[2]/form/div[1]/input')
        # Write "Server 1" to the input element
        input_element.clear()  # Clear any existing text
        input_element.send_keys("Server 1")

        input_element2 = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[2]/div[1]/div[1]/div[2]/form/div[2]/input')
        # Write "1" to input_element2
        input_element2.clear()  # Clear any existing text
        input_element2.send_keys("1")   

        select_element = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[2]/div[1]/div[1]/div[2]/form/div[3]/select')
        # Create a Select object
        select = Select(select_element)
        # Select "Youtube" from the dropdown by its value
        select.select_by_value("youtube")

        input_element3 = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[2]/div[1]/div[1]/div[2]/form/div[4]/input')

        # Assuming you have the corresponding "movie_link" value from your CSV
        youtube_link = row['YOUTUBE_URL']# Replace with the actual value from your CSV

        # Write the "movie_link" value to the input element
        input_element3.clear()  # Clear any existing text
        input_element3.send_keys(youtube_link)

        add_button = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[2]/div[1]/div[1]/div[2]/form/div[6]/button')
        add_button.click()
        time.sleep(3)

        wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
        next_button = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[4]/div/div[4]/div/button')))
        next_button.click()
        

        input_element4 = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[2]/div[2]/div[1]/div[2]/div/form/div[1]/input')
        # Write "Drive" to input_element4
        input_element4.clear()  # Clear any existing text
        input_element4.send_keys("Drive")

        input_element5 = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[2]/div[2]/div[1]/div[2]/div/form/div[2]/input')
        # Write "480p" to input5
        input_element5.clear()  # Clear any existing text
        input_element5.send_keys("480p")

        input_element6 = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[2]/div[2]/div[1]/div[2]/div/form/div[3]/input')
        # Write "480p" to input5
        input_element6.clear()  # Clear any existing text
        input_element6.send_keys("300MB")


        input_element7 = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[2]/div[2]/div[1]/div[2]/div/form/div[4]/input')
        movie_link = row['MOVIE_LINK']
        # Write the "movie_link" from the CSV row to input_element6
        input_element7.clear()  # Clear any existing text
        input_element7.send_keys(movie_link)


        select_element2 = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[2]/div[2]/div[1]/div[2]/div/form/div[5]/select')
        # Create a Select object
        select = Select(select_element2)
        # Select "In app download" from the dropdown by its visible text
        select.select_by_visible_text("In app download")
        time.sleep(1)

    
        button_element2 = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[2]/div[2]/div[1]/div[2]/div/form/button')
        button_element2.click()
        time.sleep(3)

        wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
        next_button = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[4]/div/div[4]/div/button')))
        next_button.click()

        driver.get('https://flexcinemaz.com/admin/videos_add/')
        i += 1
        
        wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
        next_button = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[4]/div/div[4]/div/button')))
        next_button.click()
        
# Close the WebDriver
driver.quit()

print("Completed the task.")


