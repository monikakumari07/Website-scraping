Project :Web Scraper for Extracting Website Information

Description:
This project extracts specific information from a list of websites and stores the data in a MySQL database. The information includes the robots.txt URL, sitemap URL, contact email, contact address, contact number, language, CMS/MVC, and website category.


## Requirements
- Python 3.x
- MySQL Server
- `requests` library
- `BeautifulSoup` library
- `scrapy` library
- `mysql-connector-python` library

## Setup Instructions

1. Clone the repository and navigate to the project directory:
    ```bash
    git clone <repository_url>
    cd website-scraper
    ```

2. Install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

3. Create a MySQL database and table using the SQL script:
    ```sql
    source sql/create_tables.sql;
    ```

4. Update the `config/db_config.py` file with your MySQL username and password.

5. Run the Python script to start scraping:
    ```bash
    python scraper.py
    ```

## Code Explanation

- `scrape_website(url)`: This function scrapes the given URL and extracts the required information.
- `get_robots_txt_url(base_url)`: Constructs the robots.txt URL.
- `get_sitemap_url(base_url)`: Extracts the sitemap URL from the robots.txt file.
- `get_contact_info(soup)`: Extracts contact email, address, and phone number from the HTML.
- `get_language(soup)`: Extracts the language from the HTML.
- `get_cms_mvc(soup)`: Attempts to identify the CMS or MVC framework used.
- `get_category(url)`: Placeholder function for category detection.
- `store_data(data)`: Stores the extracted information in the MySQL database.

## Challenges

- Parsing contact information can be challenging due to the varied ways in which websites present this data.
- Identifying CMS/MVC frameworks accurately requires more robust detection logic, which can be complex.
