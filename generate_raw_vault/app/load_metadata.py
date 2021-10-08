import json
import itertools


class Metadata:
    def __init__(self, metadata):
        self.metadata = metadata

    def get_business_topics(self):
        business_topics = self.metadata.get("business_topics")
        return business_topics

    def get_source_business_topics(metadata):
        topics = [topic for topic in metadata.get("business_topics").values()]
        return topics

    def get_hubs_from_business_topics(self):
        business_topics = self.get_business_topics()
        list_business_topics = list(business_topics.keys())
        return list_business_topics

    def get_sats_from_hub(self, hub):
        business_topics = self.get_business_topics()
        topics = business_topics.get(hub)
        sats = [
            topic.get("business_definition")
            for topic in topics.get("business_attributes")
        ]
        return sats


def load_metadata_file(metadata_path: str):
    with open(metadata_path) as metadata_file:
        metadata = json.load(metadata_file)
    return metadata


if __name__ == "__main__":
    metadata_file = load_metadata_file("./source_metadata/customers_v1.json")
    metadata = Metadata(metadata_file)
    print(metadata.get_business_topics(), "\n")
    # print(metadata.get_hubs_from_business_topics(), '\n')
    # print(metadata.get_sats_from_hub("CUSTOMER"), '\n')
    # print(metadata.get_sats_from_hub("PRODUCT"), '\n')
