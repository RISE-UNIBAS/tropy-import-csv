from __future__ import annotations
from typing import List, Optional, Dict, Union, Tuple
from json import load, dump
import os.path
import csv

DIR = os.path.dirname(__file__)


class Utility:
    """ A collection of utility functions. """

    @staticmethod
    def load_json(file_path: str) -> list:
        """ Load a JSON object from file.

        :param file_path: complete path to file including filename and extension
        """

        with open(file_path, encoding="utf-8") as file:
            loaded = load(file)

            return loaded

    @staticmethod
    def save_json(data: Union[List, Dict],
                  file_path: str) -> None:
        """ Save data as JSON file.

        :param data: the data to be saved
        :param file_path: complete path to file including filename and extension
        """

        with open(file_path, "w") as file:
            dump(data, file)


def csv2json(csv_path: str, json_path: str) -> None:
    """ Convert CSV to JSON-LD.

    :param csv_path: complete path to CSV file including filename and extension
    :param json_path: complete path to JSON-LD file including filename and extension
    """

    # TODO: assert structure specifications of csv

    with open(csv_path, encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=",")
        next(reader)
        graph = []
        for line in reader:
            item = dict()
            item["@type"] = "Item"
            item["template"] = "https://tropy.org/v1/templates/generic"
            item["title"] = line[0]
            item["creator"] = line[1]
            item["date"] = line[2]
            item["type"] = line[3]
            item["source"] = line[4]
            item["collection"] = line[5]
            item["box"] = line[6]
            item["folder"] = line[7]
            item["identifier"] = line[8]
            item["rights"] = line[9]
            photos = []
            for photo_title in line[10].split(";"):
                photo = Utility.load_json(DIR + "/tropy-photo.json")
                photo["title"] = photo_title
                photos.append(photo)
            item["photo"] = photos
            graph.append(item)

        context = Utility.load_json(DIR + "/tropy-generic-context.json")
        data = {"@context": context, "@graph": graph, "version": "1.11.1"}
        Utility.save_json(data, json_path)
