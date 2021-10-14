import json
import itertools
from generate_raw_vault.app.find_metadata_files import load_metadata_file


class Metadata:
    def __init__(self, metadata):
        self.metadata = metadata

    def get_source_name(self):
        return self.metadata.get("source_name")

    def get_target_schema(self):
        return self.metadata.get("destination_schema")

    def get_target_database(self):
        return self.metadata.get("destination_database")

    def get_business_topics(self):
        business_topics = self.metadata.get("business_topics")
        return business_topics

    def get_versioned_source_name(self):
        source_name = self.metadata.get("source_name")
        version = "".join(["V", self.metadata.get("version")])
        versioned_source_name = "_".join([source_name, version])
        return versioned_source_name

    def get_source_business_topics(self):
        topics = [topic for topic in self.metadata.get("business_topics").values()]
        return topics

    def get_hubs_from_business_topics(self):
        business_topics = self.get_business_topics()
        list_business_topics = list(business_topics.keys())
        return list_business_topics

    def get_sats_from_source(self):
        hubs = self.get_hubs_from_business_topics()
        sats = {hub: self.get_sat_from_hub(hub) for hub in hubs}
        return sats

    def get_sat_from_hub(self, hub):
        business_topics = self.get_business_topics()
        topics = business_topics.get(hub)
        sats = [
            topic.get("business_definition")
            for topic in topics.get("business_attributes")
        ]
        return sats

    def get_business_keys(self):
        business_topics = self.get_business_topics()
        topics = business_topics.keys()
        business_keys = {
            topic: business_topics.get(topic).get("business_keys") for topic in topics
        }
        return business_keys

    def get_hub_business_key(self, hub_name):
        primary_key = [key for key in self.get_business_keys().get(hub_name).keys()][0]
        return primary_key

    def get_source_attributes(self):
        topics = self.get_source_business_topics()
        flattened_business_attributes = self.flatten_business_attributes()
        source_attributes = [
            self.get_attributes(attr) for attr in flattened_business_attributes
        ]
        flatten_source_attributes = list(itertools.chain(*source_attributes))
        return flatten_source_attributes

    def get_attributes(self, attr):
        source_attributes = [{key: value} for key, value in attr.get("payload").items()]
        return source_attributes

    def flatten_business_attributes(self):
        topics = self.get_source_business_topics()
        business_attributes = [topic.get("business_attributes") for topic in topics]
        flatten_business_attributes = list(itertools.chain(*business_attributes))
        return flatten_business_attributes


if __name__ == "__main__":
    metadata_file = load_metadata_file(
        "generate_raw_vault/tests/fixtures/metadata_testfile.json"
    )
    metadata = Metadata(metadata_file)
    print(metadata.flatten_business_attributes())
