# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import re
from datetime import datetime

# OBS UNTESTED
class CheckItemPipeLine:
    def process_item(self, article, spider):
        if not article['url']:
            raise DropItem['Missing Url attribute in article']

        if not article['title']:
            raise DropItem['Missing Title attribute in article']

        if not article['text']:
            raise DropItem['Missing Text attribute in article']

        if not article['lastUpdated']:
            raise DropItem['Missing Url attribute in article']

        return article


# Removes additional information scraped from articles last updated date
class CleanDatePipeLine:
    def process_item(self, article, spider):
        print("Entered CleanDataPipeLine")
        article['lastUpdated'] = article['lastUpdated'].replace('GMT ', '').replace('Updated ', '').strip()
        # article['lastUpdated'] = article['lastUpdated'].replace(' ', '')
        article["lastUpdated"] = re.sub('\([0-9A-Z" "]+\)', '', article['lastUpdated'])
        print("Stored in article[lastUpdated]: " + article["lastUpdated"])

        # article['lastUpdated'].replace('\([0-9A-Z" "]+\)', "")
        return article

# Reformat scraped lastUpdated to time object
class ReformatDatePipeLine:
    def process_item(self, article, spider):
        datestr = article['lastUpdated'].split()
        if len(datestr[3]) < 3:
            datestr[3] = "".join(("0", datestr[3]))

        datestr = " ".join(datestr)
        article['lastUpdated'] = datetime.strptime(datestr, '%H%M  %B %d, %Y')
        return article
