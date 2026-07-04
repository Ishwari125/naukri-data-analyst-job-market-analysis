# Naukri.com Data Analyst Job Market Analysis

An end-to-end data analysis project that scrapes live Data Analyst job postings from Naukri.com and analyzes them to uncover in-demand skills, salary trends, hiring hotspots, and work-mode preferences in the Indian job market.

## Project Overview

Most beginner data analysis projects use pre-cleaned Kaggle datasets. This project instead starts from scratch: scraping real, messy, live job posting data directly from the web, then cleaning and analyzing it to answer questions genuinely useful to a job seeker.

## Business Questions Answered

1. What are the most in-demand skills for Data Analyst roles?
2. What experience level do most postings actually require?
3. Which cities have the most Data Analyst openings?
4. Which companies are hiring most aggressively for this role?
5. Where salary is disclosed, what does it look like, and how does it change with experience?
6. What's the split between Remote, Hybrid, and On-site openings?

## Key Findings

- **Top skill in demand:** Data Analysis, followed by Python, Power BI, and SQL
- **Fresher-friendly market:** A large share of postings require 0 years of experience
- **Top hiring city:** Bengaluru, followed by Pune and Hyderabad
- **Top hiring company:** Wipro
- **Average minimum salary (where disclosed):** ~₹7 Lacs per annum, rising with experience
- **Work mode:** The large majority of postings are On-site, with only a small share offering Remote or Hybrid options
- Only ~13% of postings disclosed salary at all — a notable market transparency gap

## Tech Stack

- **Web Scraping:** Selenium, BeautifulSoup (Selenium was required because Naukri renders job listings via JavaScript; a simple requests-based scraper returns an empty page)
- **Data Cleaning & Analysis:** Pandas
- **Visualization:** Matplotlib, Seaborn

## Project Workflow

1. **Scraping** (`naukri_job_scraper_selenium.py`) – Uses Selenium to load Naukri's search result pages (which are JavaScript-rendered) and BeautifulSoup to parse job cards into structured data: title, company, experience, salary, location, description, skills, and posting date.
2. **Data Cleaning** – Removed duplicates, handled missing values contextually (e.g. missing salary is treated as "not disclosed" rather than an error), converted experience ranges into numeric min/max columns, standardized inconsistent skill-tag casing (e.g. "data analysis" vs "Data Analysis"), merged near-duplicate skill tags, and removed generic filler tags that added noise.
3. **Exploratory Analysis & Visualization** – Answered each business question with a corresponding chart (bar charts, a pie chart, and a line chart), saved to the `charts/` folder.

## Notable Data Quality Issues Found & Fixed

Real scraped data is messy. A few examples of issues caught and resolved during this project:

- **JavaScript rendering:** An initial `requests`-only scraper returned zero job listings because Naukri loads job cards via JavaScript after the page loads. Fixed by switching to Selenium to render the page first.
- **Case-duplicate skills:** The same skill appeared multiple times under different capitalizations (e.g. "SQL", "Sql", "sql"), inflating the apparent skill diversity. Fixed by standardizing text case and merging known near-duplicate tags.
- **Mixed-unit salary values:** A few postings listed salary as e.g. `"50000-2 Lacs PA"`, mixing plain rupees and Lacs in the same field. Left unhandled, this would have skewed the average salary calculation by roughly 100x. Filtered out during cleaning.

## Files in This Repository

| File | Description |
|---|---|
| `naukri_job_scraper_selenium.py` | Scrapes job postings from Naukri.com |
| `naukri_analysis.ipynb` | Full data cleaning and analysis (Steps 1–3) |
| `naukri_data_analyst_jobs.csv` | Raw scraped data |
| `naukri_cleaned.csv` | Cleaned, analysis-ready data |
| `charts/` | All generated visualizations |
| `requirements.txt` | Python dependencies |

## How to Run This Project

```bash
# install dependencies
pip install -r requirements.txt

# run the scraper (requires Google Chrome installed)
python naukri_job_scraper_selenium.py

# then open and run naukri_analysis.ipynb in Jupyter Notebook
```

## Limitations

- Data reflects a single snapshot in time (one scrape date), not a historical trend
- Only ~13% of postings disclosed salary, so salary-based findings are based on a smaller sample
- Limited to the "Data Analyst" role search term on Naukri.com

## Future Improvements

- Compare across multiple roles (Data Analyst vs Business Analyst vs Data Scientist)
- Track job postings over time to identify hiring trends
- Deploy an interactive dashboard (Streamlit) for live filtering by city, skill, and experience level

## Author

[Your Name] — [LinkedIn URL] — [GitHub URL]