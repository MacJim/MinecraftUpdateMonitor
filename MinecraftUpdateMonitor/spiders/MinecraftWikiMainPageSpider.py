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
            javaEditionRelativeURLs = response.xpath("//div[@class='edition-group']/div[@class='edition-box'][1]/div/div/a[@title='Java']/../b/a[@href and @title]/@href").extract()

            if ((len(javaEditionVersionStrings) == 1) and (len(javaEditionRelativeURLs) == 1)):
                # Only a release version is available.
                yield {
                    "releaseVersionString": javaEditionVersionStrings[0],
                    "releaseVersionURL": "https://minecraft.gamepedia.com" + javaEditionRelativeURLs[0]
                }

            elif ((len(javaEditionVersionStrings) == 2) and (len(javaEditionRelativeURLs) == 2)):
                # Both a release version and a development version are available.
                yield {
                    "releaseVersionString": javaEditionVersionStrings[0],
                    "releaseVersionURL": "https://minecraft.gamepedia.com" + javaEditionRelativeURLs[0],
                    "developmentVersionString": javaEditionVersionStrings[1],
                    "developmentVersionURL": "https://minecraft.gamepedia.com" + javaEditionRelativeURLs[1]
                }

            else:
                yield {}

        except:
            yield {}
