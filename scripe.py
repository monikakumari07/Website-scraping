import requests
from bs4 import BeautifulSoup
import re
import mysql.connector
from config.db_config import DB_CONFIG
import phonenumbers

def read_websites_from_file(filename):
    with open(filename, 'r') as file:
        websites = [line.strip() for line in file.readlines()]
    return websites

websites_to_scrape = read_websites_from_file('websites.txt')

def get_robots_txt_url(base_url):
    return f"{base_url}/robots.txt"

def get_sitemap_url(base_url):
    robots_url = get_robots_txt_url(base_url)
    response = requests.get(robots_url)
    if response.status_code == 200:
        for line in response.text.split('\n'):
            if line.lower().startswith('sitemap:'):
                return line.split(': ')[1]
    return None

def get_contact_info(soup):
    email = None
    address = None
    phone = None
    # Extract email
    
    try:
        email = soup.select("a[href*=mailto]")[-1].text.strip() 
    except:
        pass

    if not email:
        try:
            email_tag = soup.find('a', href=re.compile(r'mailto:'))
            if email_tag:
                email = email_tag['href'].replace('mailto:', '').strip()
        except:
            pass

    if not email:
        try:
            mail_list = re.findall(r'\w+@\w+\.\w+', str(soup))
            if mail_list:
                email = mail_list[-1]
        except:
            pass

    # Extract address
    address_pattern = r'\d+\s+[\w\s]+\s*,?\s*\w+\s*\d+'
    try:
        address = re.findall(address_pattern, str(soup))[-1]
    except IndexError:
        pass
    
    # Extract phone number
    try:
        phone = soup.select("a[href*=callto]")[0].text
    except:
        pass

    if not phone:
        try:
            phone = re.findall(r'\(?\b[2-9][0-9]{2}\)?[-][2-9][0-9]{2}[-][0-9]{4}\b', str(soup))[0]
        except:
            pass

    if not phone:
        try:
            phone = re.findall(r'\(?\b[2-9][0-9]{2}\)?[-. ]?[2-9][0-9]{2}[-. ]?[0-9]{4}\b', str(soup))[-1]
        except:
            print ('Phone number not found')
            phone = ''

    # Use placeholders if data is missing
    email = email if email else "N/A"
    address = address if address else "N/A"
    phone = phone if phone else "N/A"

    return email, address, phone

def get_language(soup):
    return soup.html.get('lang', 'en')

def get_cms_mvc(soup):
    generator_meta = soup.find('meta', {'name': 'generator'})
    if generator_meta:
        return generator_meta['content']
    return 'Unknown'

def get_category(url):
    return 'General'

def scrape_website(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to scrape {url}. Status code: {response.status_code}")
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        robots_url = get_robots_txt_url(url)
        sitemap_url = get_sitemap_url(url)
        email, address, phone = get_contact_info(soup)
        language = get_language(soup)
        cms_mvc = get_cms_mvc(soup)
        category = get_category(url)
        
        data = {
            'url': url,
            'robots_url': robots_url if robots_url else '',
            'sitemap_url': sitemap_url if sitemap_url else '',
            'contact_email': email if email else '',
            'contact_address': address if address else '',
            'contact_number': phone if phone else '',
            'language': language if language else 'en',
            'cms_mvc': cms_mvc if cms_mvc else 'Unknown',
            'category': category
        }
        
        return data
    
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return None

def store_data(data):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM website_info WHERE url = %s", (data['url'],))
        existing_entry = cursor.fetchone()

        if existing_entry:
            print(f"URL {data['url']} already exists in database. Skipping insertion.")
            return
        sql = ("INSERT INTO website_info (url, robots_url, sitemap_url, contact_email, contact_address, "
               "contact_number, language, cms_mvc, category) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        
        val = (
            data['url'], data['robots_url'], data['sitemap_url'], data['contact_email'],
            data['contact_address'], data['contact_number'], data['language'],
            data['cms_mvc'], data['category']
        )
        
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"Data stored successfully for URL: {data['url']}")
        
    except mysql.connector.Error as err:
        print(f"Error storing data for URL {data['url']}: {err}")

# Loop through each website, scrape data, and store it
for website in websites_to_scrape:
    print(f"Scraping {website}...")
    data = scrape_website(website)
    
    if data:
        print(f"Storing data for {website}...")
        store_data(data)
    else:
        print(f"Failed to scrape {website}")
