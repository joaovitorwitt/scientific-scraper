from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import datetime
import random


# GATHER MOST RECENT ONLINE STORIES FROM https://pubs.aip.org/physicstoday
# title, author, and link

# PARENT CLASS = widget-dynamic-content-advanced-view
# WRAPER CLASS = widget-dynamic-entry-wrap

def get_recent_articles():
    html = urlopen("https://pubs.aip.org/physicstoday")
    bs = BeautifulSoup(html, 'html.parser')
