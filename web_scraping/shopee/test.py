from seleniumwire import webdriver
from seleniumwire.utils import decode
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from memory_profiler import profile

from datetime import datetime
import pandas as pd
import json
import time
import re

from seleniumwire import webdriver  # Import from seleniumwire

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# Go to the Google home page
driver.get('https://www.shopee.vn')
time.sleep(5)
