---

# FlexCinemaz Automation Project

This project aims to automate the process of uploading movies to the FlexCinemaz website. The application is built using Python and PyQt5 for the UI interface and uses Selenium for web automation. The primary goal is to reduce the manual effort involved in adding thousands of movies to the FlexCinemaz admin dashboard.

![fLEXCINEMAZ AUTOMATION Demo](https://github.com/benny-png/Flexcinemaz-Project/blob/main/flex.png)

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [UI Interface](#ui-interface)
- [Automated Workflow](#automated-workflow)
- [Demo](#demo)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Automated Data Extraction**: Extract movie data from specified websites.
- **CSV Export**: Save the extracted movie data to CSV files.
- **Login Automation**: Automatically log into the FlexCinemaz admin dashboard.
- **Movie Upload**: Upload movies to the FlexCinemaz admin dashboard, including fetching IMDB IDs and YouTube trailers.
- **Error Handling**: Handle missing data and duplicates efficiently.

## Requirements

- Python 3.x
- PyQt5
- Selenium
- WebDriver Manager
- BeautifulSoup
- Chrome Browser (or any other browser supported by Selenium)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/FlexCinemaz-Automation.git
   cd FlexCinemaz-Automation
   ```

2. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download ChromeDriver**:
   Follow the instructions [here](https://sites.google.com/a/chromium.org/chromedriver/downloads) to download the appropriate version of ChromeDriver for your system.

4. **Update the `resource_path` function**:
   Ensure the `resource_path` function points to the correct paths for your resources, especially for Chrome.

## Usage

1. **Run the application**:
   ```bash
   python main.py
   ```

2. **UI Interface**:
   - Load the last movie uploaded.
   - Click the 'Export' button to start the automation process.
  

![fLEXCINEMAZ AUTOMATION Demo](https://github.com/benny-png/Flexcinemaz-Project/blob/main/flex.png)


## UI Interface

The UI interface is created using PyQt5. It includes functionalities to load the last movie uploaded and start the export process. The main window is designed to be user-friendly and intuitive.

## Automated Workflow

1. **Login to FlexCinemaz**:
   The application logs into the FlexCinemaz admin dashboard using provided credentials.

2. **Data Extraction**:
   - Extract movie titles, years, and links from specified websites.
   - Save the extracted data to a CSV file.

3. **Movie Upload**:
   - Read the CSV file.
   - For each movie, fetch its IMDB ID and YouTube trailer.
   - Upload the movie to FlexCinemaz admin dashboard, including enabling download options.

## Demo

![Demo Video](path-to-demo-video)
![UI Screenshot](path-to-ui-screenshot)

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. Make sure to follow the existing coding style and include tests for new features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
