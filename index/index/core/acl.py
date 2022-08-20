from typing import Dict, Union

import requests
import yaml
from yaml.loader import SafeLoader

from xml.etree import ElementTree


class ACLClient:
    def __init__(self, venues_path: str = "/venues.yaml"):

        with open(venues_path) as fh:
            self.venues = yaml.load(fh, Loader=SafeLoader)
        self.conferences = list(self.venues.keys())
        self.conference_2_acronym = {k: v["acronym"] for k, v in self.venues.items()}
        self.conference_2_name = {k: v["name"] for k, v in self.venues.items()}
        self.oldstyle_letter_2_conference = {
            v["oldstyle_letter"]: k
            for k, v in self.venues.items()
            if "oldstyle_letter" in v
        }

    def get_conference_from_filename(self, filename: str) -> str:
        # remove extension
        *filename_wo_extension, _ = filename.split(".")
        if len(filename_wo_extension) == 1:
            # old filename style, e.g. "E91.xml"
            conference = self.oldstyle_letter_2_conference[
                filename_wo_extension[0][0].upper()
            ]
        elif len(filename_wo_extension) == 2:
            # new filename style, e.g. "2022.acl.xml"
            conference = filename_wo_extension[1].lower()
        else:
            raise ValueError(f"Unknown filename style {filename}.")

        if conference not in self.conferences:
            raise ValueError(f"Unknown conference {conference}.")

        return conference

    def get_xml_from_url(self, url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()
        return response.content

    def get_text(self, element: str) -> str:
        return "".join(element.itertext())

    def find_and_get_text(self, element, tag) -> Union[str, None]:
        result = element.find(tag)
        if result is not None:
            result = self.get_text(result)
        return result

    def get_publications_from_xml(self, xml: str, conference: str) -> Dict:

        tree = ElementTree.fromstring(xml)

        for volume in tree.iter("volume"):

            meta = volume.find("meta")
            year = self.find_and_get_text(meta, "year")

            for paper in volume.iter("paper"):
                title = self.find_and_get_text(paper, "title")
                abstract = self.find_and_get_text(paper, "abstract")

                authors = []
                for author in paper.iter("author"):
                    firstname = self.find_and_get_text(author, "first")
                    lastname = self.find_and_get_text(author, "last")
                    authors.append({"firstname": firstname, "lastname": lastname})

                bibkey = self.find_and_get_text(paper, "bibkey")

                url = self.find_and_get_text(paper, "url")

                yield {
                    "conference_short": self.conference_2_acronym[conference],
                    "conference_long": self.conference_2_name[conference],
                    "year": year,
                    "title": title,
                    "abstract": abstract,
                    "authors": authors,
                    "bibkey": bibkey,
                    "url": url,
                }
