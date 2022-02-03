from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor

from scrapy.selector import Selector
from scrapy.item import Item, Field
from scrapy.http.request import Request

listings_class = "result-list-entry__brand-title-container"
allowed_domain = "immobilienscout24.de"
start_url = "https://www.immobilienscout24.de/Suche/de/berlin/berlin/wohnung-mieten"

attributes = [
    # allgemein
    'is24qa-etage',
    'is24qa-flaeche',
    'is24qa-zi',
    'is24qa-bezugsfrei-ab',

    # kosten
    'is24qa-kaltmiete',
    'is24qa-nebenkosten'

]

class ISItem(Item):
    url = Field()

    # allgemein
    is24qa_etage = Field()
    is24qa_flaeche = Field()
    is24qa_zi = Field()
    is24qa_bezugsfrei_ab = Field()

    # kosten
    is24qa_kaltmiete = Field()
    is24qa_nebenkosten = Field()

    lat = Field()
    lng = Field()
    address = Field()
    zip_region_country = Field()


class DetailsPageSpider(CrawlSpider):
    name = "is24"
    allowed_domains = [allowed_domain]
    start_urls = [ start_url ]
    rules = (
        # Extract links for next pages
        Rule(LxmlLinkExtractor(
            allow=(),
            restrict_xpaths=(".//*[@id='pager']//div//a")),
            callback='parse_listings',
            follow=True
        ),
    )

    def parse_start_url(self, response):
        return self.parse_listings(response)

    def parse_listings(self, response):
        sel = Selector(response)
        print("listing page", response.url)
        links = sel.xpath(".//*[@class='{}']".format(listings_class))
        for link in links:
            print("="*100)
            link = "https://www.immobilienscout24.de" + link.xpath("@href").extract()[0]
            print(link)
            yield Request(link, callback=self.parse_details)

    def parse_details(self, response):

        sel = Selector(response)
        print("details", response.url)

        item = ISItem()

        item['url'] = response.url

        for attribute in attributes:
            try:
                item[attribute.replace("-", "_")] = sel.css('.{}::text'.format(attribute)).extract()[0].strip()
            except Exception as e:
                item[attribute.replace("-", "_")] = None

        # address and lat long require special treatment
        address = None
        try:
            address = sel.xpath("//div[contains(@class, 'address-block')]//span[contains(@class, 'block')]//text()").extract_first().strip()
        except Exception as e:
            pass

        zip_region_country = None
        try:
            zip_region_country = sel.xpath("//div[contains(@class, 'address-block')]//span[contains(@class, 'zip-region-and-country')]//text()").extract_first().strip()
        except Exception as e:
            pass

        item['address'] = address
        item['zip_region_country'] = zip_region_country

        items = response.xpath("//script[contains(., 'getMapOptions')]/text()")
        txt = items.extract_first()
        for line in txt.split("\n"):
            if "lat: " in line:
                item['lat'] = line.split("lat: ")[1]
            if "lng: " in line:
                item['lng'] = line.split("lng: ")[1]


        return item
