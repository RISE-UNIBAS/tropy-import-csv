from __future__ import annotations
from typing import List, Optional, Dict, Union, Tuple
from json import load, dump, dumps
import os.path
import csv

DIR = os.path.dirname(__file__)


class _Utility:
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


class _Parser:
    """ A collection of parser functions. """

    @staticmethod
    def parse_photos(photos_csv: str, photos_path: str = None) -> list:
        """ Parse photos from CSV.

        :param photos_csv: photos
        :param photos_path: complete path to the photos-folder, defaults to None
        """

        photos = []
        for photo_path in photos_csv.split(";"):
            photo = _Utility.load_json(DIR + "/tropy-photo.json")
            if photos_path is None:
                photo["title"] = photo_path.split("\\")[-1]
                photo["filename"] = photo_path.split("\\")[-1]
                photo["path"] = photo_path
            else:
                photo["title"] = photo_path
                photo["filename"] = photo_path
                photo["path"] = photos_path + photo_path
            photos.append(photo)
        return photos


class Transform:
    """ A collection of transformation functions. """

    @staticmethod
    def csv2json(csv_path: str,
                 json_path: Union[str, None],
                 photos_path: str = None,
                 interactive: bool = False) -> Optional[Union[str, dict]]:
        """ Convert CSV to JSON-LD.

        :param csv_path: complete path to CSV file including filename and extension
        :param json_path: complete path to JSON-LD file including filename and extension or None to return as string
        :param photos_path: complete path to the photos-folder (format "/Path/to/photos/"), defaults to None
        :param interactive: toggle interactive mode, defaults to False
        """

        try:
            file = open(csv_path, encoding="utf-8")
            reader = csv.reader(file, delimiter=",")
        except (FileNotFoundError, OSError):
            reader = csv.reader(csv_path.splitlines(), delimiter=",")

        header = next(reader)
        assert header == Transform.required_csv_header(), "Error: CSV not formatted to specification!"
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
            # TODO: tags
            item["photo"] = _Parser.parse_photos(line[11], photos_path=photos_path)
            # TODO: notes

            graph.append(item)

        context = _Utility.load_json(DIR + "/tropy-generic-context.json")
        data = {"@context": context, "@graph": graph, "version": "1.11.1"}
        if interactive is True:
            return data
        elif json_path is None:
            return dumps(data)
        _Utility.save_json(data, json_path)

    @staticmethod
    def required_csv_header():
        """ Return the required CSV header. """

        with open(DIR + "/sample.csv", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=",")
            return next(reader)

