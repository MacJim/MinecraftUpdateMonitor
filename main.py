import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from MinecraftUpdateMonitor.helpers.DatabaseManager import DatabaseManager
from MinecraftUpdateMonitor.spiders.MinecraftWikiMainPageSpider import MinecraftWikiMainPageSpider


# 1. Switch to project directory.
mainFilePath = os.path.dirname(os.path.abspath(__file__))
os.chdir(mainFilePath)

# 2. Create database if it's not created.
if (not os.path.isfile(os.path.join(os.getcwd(), DatabaseManager.databaseFilename))):
    print("This seems to be the first time you run this script. Would you like to create the database file in the project folder? (Yes/No) ")

    userInput = input()

    if ((userInput == "Yes") or (userInput == "yes") or (userInput == "Y") or (userInput == "y")):
        # 2-1. Execute "Documentation/Create tables.sql" file.
        DatabaseManager.getInstance().createTables()
    else:
        # 2-2. Prompt and exit.
        print("You have chosen NOT to create the database file. You may create it manually using the following command:\nsqlite3 MinecraftUpdateMonitor.db < Documentation/Create\\ tables.sql")
        exit()

# 3. Start crawling.
crawlerProcess = CrawlerProcess(get_project_settings())
crawlerProcess.crawl(MinecraftWikiMainPageSpider)
crawlerProcess.start()
