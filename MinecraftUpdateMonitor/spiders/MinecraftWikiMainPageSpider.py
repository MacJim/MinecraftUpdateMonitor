import scrapy


class MinecraftWikiMainPageSpider (scrapy.Spider):
    """This class parses the Minecraft Wiki main page (https://minecraft.gamepedia.com/Minecraft_Wiki) to obtain the latest Minecraft stable and development version numbers.
    """

    custom_settings = {
        "ITEM_PIPELINES": {
            "MinecraftUpdateMonitor.pipelines.MinecraftWikiMainPagePipeline.MinecraftWikiMainPagePipeline": 100
        }
    }

    name = "MinecraftWikiMainPage"

    def start_requests(self):
        yield scrapy.Request(url="https://minecraft.gamepedia.com/Minecraft_Wiki", callback=self.parse)

    def parse(self, response):
        try:
            releaseVersionString = response.xpath("//div[@class='edition-group']/div[@class='edition-box'][1]/div/div[1]/b/a[@href and @title]/text()").extract()[0]
            releaseVersionRelativeURL = response.xpath("//div[@class='edition-group']/div[@class='edition-box'][1]/div/div[1]/b/a[@href and @title]/@href").extract()[0]
            releaseVersionFullURL = "https://minecraft.gamepedia.com" + releaseVersionRelativeURL
            developmentVersionString = response.xpath("//div[@class='edition-group']/div[@class='edition-box'][1]/div/div[2]/b/a[@href and @title]/text()").extract()[0]
            developmentVersionRelativeURL = response.xpath("//div[@class='edition-group']/div[@class='edition-box'][1]/div/div[2]/b/a[@href and @title]/@href").extract()[0]
            developmentVersionFullURL = "https://minecraft.gamepedia.com" + developmentVersionRelativeURL

            yield {
                "releaseVersionString": releaseVersionString,
                "releaseVersionURL": releaseVersionFullURL,
                "developmentVersionString": developmentVersionString,
                "developmentVersionURL": developmentVersionFullURL
            }

        except:
            yield {}
