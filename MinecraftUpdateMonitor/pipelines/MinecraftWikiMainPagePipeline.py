from scrapy.exceptions import DropItem
from ..helpers.DatabaseManager import DatabaseManager


class MinecraftWikiMainPagePipeline:
    def process_item(self, item, spider):
        # 1. Release version.
        latestReleaseVersionInformationInDatabase = DatabaseManager.getInstance().getLatestMinecraftReleaseVersionInformation()
        scrapedReleaseVersionString = item["releaseVersionString"]

        if ((latestReleaseVersionInformationInDatabase is None) or ("versionString" not in latestReleaseVersionInformationInDatabase) or (not (latestReleaseVersionInformationInDatabase["versionString"] == scrapedReleaseVersionString))):
            # Latest version is not in database.
            releaseVersionWikiPageURL = item["releaseVersionURL"]
            DatabaseManager.getInstance().addMinecraftReleaseVersionInformation(scrapedReleaseVersionString, releaseVersionWikiPageURL)

        # 2. Development version.
        latestDevelopmentVersionInformationInDatabase = DatabaseManager.getInstance().getLatestMinecraftDevelopmentVersionInformation()
        scrapedDevelopmentVersionString = item["developmentVersionString"]

        if ((latestDevelopmentVersionInformationInDatabase is None) or ("versionString" not in latestDevelopmentVersionInformationInDatabase) or (not(latestDevelopmentVersionInformationInDatabase["versionString"] == scrapedDevelopmentVersionString))):
            # Latest version is not in database.
            developmentVersionWikiPageURL = item["developmentVersionURL"]
            DatabaseManager.getInstance().addMinecraftDevelopmentVersionInformation(scrapedDevelopmentVersionString, developmentVersionWikiPageURL)

        return item