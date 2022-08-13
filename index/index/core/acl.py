import requests

from index.settings import AppSettings
from xml.etree import ElementTree


class ACLClient:
    def __init__(self) -> None:
        self.settings = AppSettings()

    def get_xml_from_url(self, url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()
        return response.content

    def get_text(self, element: str):
        return "".join(element.itertext())

    def find_and_get_text(self, element, tag):
        return self.get_text(element.find(tag))

    def parse_year_conference(self, element):
        year, conference = element.attrib["id"].split(".")
        return year, conference

    def get_publications_from_xml(self, xml: str) -> dict:
        tree = ElementTree.fromstring(xml)
        year, conference = self.parse_year_conference(tree)

        for volume in tree.iter("volume"):
            volume_str = volume.get("id")

            for paper in volume.iter("paper"):
                title = self.find_and_get_text(paper, "title")

                authors = []
                for author in paper.iter("author"):
                    firstname = self.find_and_get_text(author, "first")
                    lastname = self.find_and_get_text(author, "last")
                    authors.append({"firstname": firstname, "lastname": lastname})

                bibkey = self.find_and_get_text(paper, "bibkey")

                url = self.find_and_get_text(paper, "url")

                yield {
                    "conference": conference,
                    "year": year,
                    "volume": volume_str,
                    "title": title,
                    "authors": authors,
                    "bibkey": bibkey,
                    "url": url,
                }
