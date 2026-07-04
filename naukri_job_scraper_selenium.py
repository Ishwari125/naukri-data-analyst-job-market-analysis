# =====================================================
# NAUKRI.COM SCRAPER (Selenium version) - "Data Analyst" Jobs
# =====================================================
# WHY SELENIUM AND NOT REQUESTS?
# Naukri loads job listings using JavaScript AFTER the page loads
# (it's a React app). The 'requests' library only sees the raw HTML
# before JS runs, so it always finds 0 job cards.
# Selenium opens a REAL Chrome browser, waits for JS to load the
# jobs, and THEN we grab the HTML — this is why it works.
#
# SETUP (run once in terminal):
#   pip install selenium webdriver-manager pandas beautifulsoup4
#
# You do NOT need to manually download chromedriver — webdriver-manager
# handles that automatically the first time you run this script.
# =====================================================

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# ---------------------------------------------------
# SETTINGS
# ---------------------------------------------------

NUM_PAGES = 50                # how many pages to scrape (~20 jobs per page)
SEARCH_ROLE = "data-analyst"  # role we're searching for

# ---------------------------------------------------
# SET UP THE CHROME BROWSER (controlled by Selenium)
# ---------------------------------------------------

chrome_options = Options()
# run in "headless" mode = browser runs in background, no visible window
# (comment out the line below if you want to WATCH it scrape, useful for debugging)
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

# automatically download and set up the correct chromedriver version
service = Service(ChromeDriverManager().install())

# start the browser
driver = webdriver.Chrome(service=service, options=chrome_options)

all_jobs = []

# ---------------------------------------------------
# SCRAPING LOOP
# ---------------------------------------------------

for page in range(1, NUM_PAGES + 1):

    url = f"https://www.naukri.com/{SEARCH_ROLE}-jobs-{page}"
    print(f"Scraping page {page} -> {url}")

    # open the page in the browser
    driver.get(url)

    # wait for the page to fully load and JS to render the job cards
    # (a simple fixed wait is easiest for beginners; 5-7 seconds is usually enough)
    time.sleep(6)

    # now grab the FULLY RENDERED page HTML (after JS ran)
    page_source = driver.page_source

    # parse it with BeautifulSoup, same as before
    soup = BeautifulSoup(page_source, "html.parser")

    # find all job cards
    job_cards = soup.find_all("div", class_="cust-job-tuple")
    print(f"Found {len(job_cards)} job cards on page {page}")

    for card in job_cards:

        title_tag = card.find("a", class_="title")
        title = title_tag.get_text(strip=True) if title_tag else None

        company_tag = card.find("a", class_="comp-name")
        company = company_tag.get_text(strip=True) if company_tag else None

        exp_tag = card.find("span", class_="expwdth")
        experience = exp_tag.get_text(strip=True) if exp_tag else None

        salary_tag = card.find("span", class_="sal-wrap")
        salary = salary_tag.get_text(strip=True) if salary_tag else None

        location_tag = card.find("span", class_="locWdth")
        location = location_tag.get_text(strip=True) if location_tag else None

        desc_tag = card.find("span", class_="job-desc")
        description = desc_tag.get_text(strip=True) if desc_tag else None

        skills_tags = card.find_all("li", class_="dot-gt")
        skills = ", ".join([s.get_text(strip=True) for s in skills_tags]) if skills_tags else None

        posted_tag = card.find("span", class_="job-post-day")
        posted = posted_tag.get_text(strip=True) if posted_tag else None

        job_data = {
            "title": title,
            "company": company,
            "experience": experience,
            "salary": salary,
            "location": location,
            "description": description,
            "skills": skills,
            "posted": posted,
        }

        all_jobs.append(job_data)

    # polite random delay before next page
    time.sleep(random.uniform(2, 4))

# close the browser once done
driver.quit()

# ---------------------------------------------------
# SAVE TO CSV
# ---------------------------------------------------

df = pd.DataFrame(all_jobs)
print(f"\nTotal jobs scraped: {len(df)}")
print(df.head())

df.to_csv("naukri_data_analyst_jobs.csv", index=False)
print("Saved to naukri_data_analyst_jobs.csv")
