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


def csv2json(file_path: str):
    """

    :param file_path:
    """

    # assert structure
    pass

    with open(file_path, encoding="utf-8") as file:
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
            images = []
            for image in line[10].split(";"):
                images.append({"@type": "Photo", "filename": image})
            item["photo"] = images
            graph.append(item)

        return graph


context = Utility.load_json(DIR + "/tropy-generic-context.json")
data = {"@context": context, "@graph": csv2json(DIR + "/test.csv"), "version": "1.11.1"}
Utility.save_json(data, DIR + "/test.json")


# TODO: import of test.json without error, but objects are not there; perhaps missing metadata for photos?



