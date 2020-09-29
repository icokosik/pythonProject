import json
import test
import dynamoDB
import boto3
import random
import scraper
from decimal import *

propertyItems = []

def addDummyItem():
    prop = {}
    prop['id'] = str(random.randint(1000, 100000))
    prop['URL'] = 'url1'
    prop['name'] = 'name1'
    prop['price'] = random.randint(1, 150)
    prop['size'] = random.randint(1, 150)
    print(prop)
    propertyItems.append(prop)

def test1():
    addDummyItem()
    addDummyItem()

    dynamoDB.insertIntoProperties(propertyItems)

def scrapingWillhaben():
    scraper.test()