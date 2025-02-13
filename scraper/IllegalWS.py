'''
Created on Feb 11, 2025

@author: kevin
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import time

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration

chrome_options.add_argument("--window-size=1920,1080")  # Set window size

# Set up the WebDriver (e.g., Chrome)
driver = webdriver.Chrome(options=chrome_options)  # Make sure chromedriver is installed

#applies stealth settings to the driver

stealth(
    driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)

print("1")

# Open the Google Reviews page
url = "https://www.google.com/search?gs_ssp=eJzj4tVP1zc0zEjJsjTPLsk1YLRSNaiwsDBKSjM1Mk4zs0xONrQwtjKoSLFMTUxJNTK1NE5KNTA0NPJiK87IzCtPBAAnZBHq&q=shinwa&rlz=1C1UEAD_enCA1144CA1144&oq=shinwa&gs_lcrp=EgZjaHJvbWUqGAgBEC4YJxivARjHARjJAxiABBiKBRiOBTIPCAAQIxgnGOMCGIAEGIoFMhgIARAuGCcYrwEYxwEYyQMYgAQYigUYjgUyBggCEEUYQDIHCAMQABiABDIHCAQQABiABDIHCAUQABiABDIHCAYQABiABDIGCAcQRRg80gEIMzkwMmowajeoAgiwAgE&sourceid=chrome&ie=UTF-8#lrd=0x882bf523f69cc183:0xd9eade2593be0112,1,,,,"

# Navigate to the website
driver.get(url)

# Retrieve the page source
html_content = driver.page_source

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Print the parsed HTML (optional)
print(soup.prettify())

#find a way to deal with IP blocking (proxies) and how to deal with dynamic class name changing
#for multiple requests use rotatinguser agents and proxies
#Mimic Human Behavior: Randomize mouse movements, clicks, and scrolls using libraries like pyautogui.