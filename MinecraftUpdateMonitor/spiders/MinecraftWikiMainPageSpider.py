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
            javaEditionVersionStrings = response.xpath("//div[@class='edition-group']/div[@class='edition-box'][1]/div/div/a[@title='Java']/../b/a[@href and @title]/text()").extract()

            releaseVersionString = response.xpath("//div[@class='edition-group']/div[@class='edition-box'][1]/div[1]/div[1]/b/a[@href and @title]/text()").extract()[0]
            releaseVersionRelativeURL = response.xpath("//div[@class='edition-group']/div[@class='edition-box'][1]/div[1]/div[1]/b/a[@href and @title]/@href").extract()[0]

            if (len(javaEditionVersionStrings) == 2):
                # Only a release version is available.
                yield {
                    "releaseVersionString": releaseVersionString,
                    "releaseVersionURL": "https://minecraft.gamepedia.com" + releaseVersionRelativeURL
                }

            elif (len(javaEditionVersionStrings) == 3):
                # Both a release version and a development version are available.
                developmentVersionString = response.xpath("//div[@class='edition-group']/div[@class='edition-box'][1]/div[1]/div[2]/a[@href and @title][2]/text()").extract()[0]
                developmentVersionRelativeURL = response.xpath("//div[@class='edition-group']/div[@class='edition-box'][1]/div[1]/div[2]/a[@href and @title][2]/@href").extract()[0]

                yield {
                    "releaseVersionString": releaseVersionString,
                    "releaseVersionURL": "https://minecraft.gamepedia.com" + releaseVersionRelativeURL,
                    "developmentVersionString": developmentVersionString,
                    "developmentVersionURL": "https://minecraft.gamepedia.com" + developmentVersionRelativeURL
                }

            else:
                yield {}

        except:
            yield {}
