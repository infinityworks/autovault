import json
import itertools


def load_metadata_file(metadata_path: str):
    with open(metadata_path) as metadata_file:
        metadata = json.load(metadata_file)
    return metadata


def get_business_topics(metadata):
    business_topics = metadata.get("business_topics")
    return business_topics


def get_hubs_from_business_topics(business_topics):
    list_business_topics = list(business_topics.keys())
    return list_business_topics


def get_sats_from_hub(business_topics, hub):
    topics = business_topics.get(hub)
    sats = {hub: [topic.get("business_definition") for topic in topics]}
    return sats


if __name__ == "__main__":
    metadata = load_metadata_file("./source_metadata/customers.json")
    business_topics = get_business_topics(metadata)

    hubs = get_hubs_from_business_topics(business_topics)
