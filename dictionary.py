import json
from datetime import datetime, UTC
from pathlib import Path
from rapidfuzz import process
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import defaultdict

class Dictionary:
    """
    Responsible for managing the approved column definition dictionary from Alation.
    Methods are provided to perform both direct and fuzzy lookups of records by 'name'.
    'name' corresponds to a column name in Alation.
    """
    PATH = Path("dictionary.json")

    def __init__(self):
        if not self.PATH.exists():
            self.PATH.write_text('{"last_update": "", "data": []}', encoding="utf-8")

        with open(self.PATH, "r", encoding="utf-8") as dictionary:
            records = json.load(dictionary)

        self.index = {record["id"]: record for record in records["data"]}
        self.name_index = defaultdict(list)

        for record in records["data"]:
            self.name_index[record["name"]].append(record)

        self.new_record_count = 0
        self.updated_record_count = 0

    def records(self):
        """
        Returns all the records in the dictionary
        """
        return self.index.values()

    def lookup(self, lookup_value: str):
        """
        Performs a direct lookup based on the 'name' field

        Note
        ----
        This method may return multiple records all of which share the same 'name' value.
        """
        return self.name_index.get(lookup_value)

    def fuzzy_lookup(self, lookup_value: str, threshold: int):
        """
        Performs a fuzzy lookup based on the 'name' field. Only records with a 'name' value whose similarity score exceeds the threshold are returned.

        Note
        ----
        This method may return multiple records all of which share the same 'name' value.
        """
        options = set(self.name_index.keys())
        search_result = process.extractOne(lookup_value, options)

        if search_result is None:
            return None
        else:
            best_match, score, _ = search_result
            return self.lookup(best_match) if score > threshold else None

    def __format_record(self, record):
        """
        Internal method for formatting records to match schema
        """
        return {
            "id": record["id"],
            "source": urljoin("https://alation.medcity.net/",record["url"]),
            "name": record["name"],
            "description": BeautifulSoup(record["description"], "html.parser").get_text(strip=True),
            "custom_fields": record["custom_fields"],
        }

    def add(self, record):
        """
        Adds or updates records in the dictionary. Existing records are skipped
        """
        record = self.__format_record(record)
        lookup = self.index.get(record["id"])

        if lookup is None:
            self.index[record["id"]] = record
            self.new_record_count += 1
        elif lookup != record:
            self.index[record["id"]] = record
            self.updated_record_count += 1

    def save(self):
        """
        Writes to the dictionary file only if new records were added or existing records were updated.
        """
        if self.new_record_count > 0 or self.updated_record_count > 0:
            output = {
                "last_update": datetime.now(UTC).isoformat(),
                "data": list(self.index.values())
            }

            with open(self.PATH, "w", encoding="utf-8") as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
