from scrapy.exceptions import DropItem
from ..helpers.DatabaseManager import DatabaseManager
from ..helpers.NotificationHelper import showSystemNotification


class MinecraftWikiMainPagePipeline:
    def process_item(self, item, spider):
        # 1. Release version.
        latestReleaseVersionInformationInDatabase = DatabaseManager.getInstance().getLatestMinecraftReleaseVersionInformation()
        scrapedReleaseVersionString = item["releaseVersionString"]

        if ((latestReleaseVersionInformationInDatabase is None) or (latestReleaseVersionInformationInDatabase["versionString"] != scrapedReleaseVersionString)):
            # 1-1. Latest version is not in database.
            # 1-1-1. Update latest version to database.
            releaseVersionWikiPageURL = item["releaseVersionURL"]
            DatabaseManager.getInstance().addMinecraftReleaseVersionInformation(scrapedReleaseVersionString, releaseVersionWikiPageURL)

            # 1-1-2. Send a notification.
            showSystemNotification("New Minecraft release version!", scrapedReleaseVersionString)

        # 2. Development version.
        latestDevelopmentVersionInformationInDatabase = DatabaseManager.getInstance().getLatestMinecraftDevelopmentVersionInformation()
        scrapedDevelopmentVersionString = item["developmentVersionString"]

        if ((latestDevelopmentVersionInformationInDatabase is None) or (latestDevelopmentVersionInformationInDatabase["versionString"] != scrapedDevelopmentVersionString)):
            # 1-1. Latest version is not in database.
            # 1-1-1. Update latest version to database.
            developmentVersionWikiPageURL = item["developmentVersionURL"]
            DatabaseManager.getInstance().addMinecraftDevelopmentVersionInformation(scrapedDevelopmentVersionString, developmentVersionWikiPageURL)

            # 1-1-2. Send a notification.
            showSystemNotification("New Minecraft development version!", scrapedDevelopmentVersionString)

        return item