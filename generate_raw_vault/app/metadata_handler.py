import itertools
from generate_raw_vault.app.find_metadata_files import load_metadata_file


class Metadata:
    def __init__(self, metadata):
        self.metadata = metadata

    def get_source_name(self):
        return self.metadata.get("source_name").replace("-", "_")

    def get_unit_of_work(self):
        unit_of_work = self.metadata.get("unit_of_work").replace("-", "_")
        return unit_of_work

    def get_source_system(self):
        return self.metadata.get("source_system").replace("-", "_")

    def get_target_schema(self):
        return self.metadata.get("destination_schema").replace("-", "_")

    def get_target_database(self):
        return self.metadata.get("destination_database").replace("-", "_")

    def get_source_version(self):
        return self.metadata.get("version")

    def get_business_topics(self):
        business_topics = self.metadata.get("business_topics")
        return business_topics

    def get_versioned_source_name(self):
        source_name = self.get_source_name()
        version = "".join(["V", self.metadata.get("version")])
        versioned_source_name = "_".join([source_name, version])
        return versioned_source_name

    def get_source_business_topics(self):
        topics = [topic for topic in self.get_business_topics().values()]
        return topics

    def get_hubs_from_business_topics(self):
        business_topics = self.get_business_topics()
        list_business_topics = list(business_topics.keys())
        return list_business_topics

    def get_hub_alias(self, hub):
        topics = self.get_business_topics()
        hub_alias = topics.get(hub).get("alias")
        return hub_alias

    def get_sat_from_hub(self, hub):
        business_topics = self.get_business_topics()
        topics = business_topics.get(hub)
        sats = {
            topic.get("business_definition"): topic.get("payload")
            for topic in topics.get("business_attributes")
        }
        return sats

    def get_business_keys(self):
        business_topics = self.get_business_topics()
        topics = business_topics.keys()
        business_keys = {
            topic: self.get_topic_key(topic, business_topics) for topic in topics
        }
        return business_keys

    def get_topic_key(self, topic, business_topics):
        topic_key = {"natural_keys": business_topics.get(topic).get("business_keys")}
        return topic_key

    def get_primarykey_alias_map(self, hub_business_keys):
        primarykey_alias_map = {}
        for primary_key, primary_key_attributes in hub_business_keys.get(
            "natural_keys"
        ).items():
            if primary_key_attributes.get("alias"):
                primarykey_alias_map[primary_key] = primary_key_attributes.get("alias")
            else:
                primarykey_alias_map[primary_key] = primary_key
        return primarykey_alias_map

    def get_alias_primarykey_map(self, primarykey_alias_map):
        alias_primarykey_map = {
            alias: primary_key for primary_key, alias in primarykey_alias_map.items()
        }
        return alias_primarykey_map

    def get_hub_business_key(self, hub_name):
        hub_business_keys = self.get_business_keys().get(hub_name)
        return self.get_primarykey_alias_map(hub_business_keys)

    def get_source_attributes(self):
        topics = self.get_source_business_topics()
        flattened_business_attributes = self.flatten_business_attributes()
        source_attributes = [
            self.get_attributes(attr) for attr in flattened_business_attributes
        ]
        flatten_source_attributes = list(itertools.chain(*source_attributes))
        return flatten_source_attributes

    def get_attributes(self, attr):
        if "null" in attr.get("payload").keys():
            del attr["payload"]["null"]
        source_attributes = [{key: value} for key, value in attr.get("payload").items()]
        return source_attributes

    def flatten_business_attributes(self):
        topics = self.get_source_business_topics()
        business_attributes = [topic.get("business_attributes") for topic in topics]
        flatten_business_attributes = list(itertools.chain(*business_attributes))
        return flatten_business_attributes


if __name__ == "__main__":
    metadata_file = load_metadata_file("source_metadata/transactions_v1.json")
    metadata = Metadata(metadata_file).get_hub_business_key("TRANSACTION")
