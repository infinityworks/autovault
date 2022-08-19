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
        hub_topics = business_topics.get(hub)
        topics = {
            business_key: business_attributes
            for business_key, business_attributes in hub_topics.items()
            if hub_topics.get("business_attributes") is not None
        }
        if topics:
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

    def get_primarykey_datatype_map(self, hub_business_keys):
        primarykey_datatype_map = {}
        for primary_key, primary_key_attributes in hub_business_keys.get(
            "natural_keys"
        ).items():
            if primary_key_attributes.get("type"):
                primarykey_datatype_map[primary_key] = primary_key_attributes.get(
                    "type"
                )
            else:
                raise Exception(f"{primary_key}, data type missing")
        return primarykey_datatype_map

    def get_primarykey_description_map(self, hub_business_keys):
        primarykey_attributes_map = {}
        for primary_key, primary_key_attributes in hub_business_keys.get(
            "natural_keys"
        ).items():
            if primary_key_attributes.get("description"):
                primarykey_attributes_map[primary_key] = primary_key_attributes.get(
                    "description"
                )
            else:
                raise Exception(f"{primary_key}, description missing")
        return primarykey_attributes_map

    def get_hub_business_key(self, hub_name):
        hub_business_keys = self.get_business_keys().get(hub_name)
        return self.get_primarykey_alias_map(hub_business_keys)

    def get_source_attributes(self):
        flattened_business_attributes = self.flatten_business_attributes()
        source_attributes = [
            column_descriptors
            for attr in flattened_business_attributes
            if (column_descriptors := self.get_attributes(attr))
        ]
        flatten_source_attributes = list(itertools.chain(*source_attributes))
        return flatten_source_attributes

    def get_attributes(self, attr):
        if attr.get("payload"):
            source_attributes = [
                {key: value} for key, value in attr.get("payload").items()
            ]
            return source_attributes

    def flatten_business_attributes(self):
        topics = self.get_source_business_topics()
        business_attributes = [
            business_attribute
            for topic in topics
            if (business_attribute := topic.get("business_attributes"))
        ]
        flatten_business_attributes = list(itertools.chain(*business_attributes))
        return flatten_business_attributes

    def flatten_business_keys(self):
        topics = self.get_source_business_topics()
        business_keys = [topic.get("business_keys") for topic in topics]
        flatten_business_keys = list(itertools.chain(*business_keys))
        return flatten_business_keys

    def get_primary_key_tests_map(self, hub_business_keys):
        primarykey_tests_map = {}
        for primary_key, primary_key_attributes in hub_business_keys.get(
            "natural_keys"
        ).items():
            if primary_key_attributes.get("tests"):
                primarykey_tests_map = primary_key_attributes.get("tests")
            else:
                raise Exception(f"{primary_key}, tests missing")
        return primarykey_tests_map

    def get_transactional_payloads(self):
        transaction_payloads = self.metadata.get("transactional_payload")
        return transaction_payloads

    def get_transactional_payload_datatype_map(self, transactional_payloads):
        transactional_payload_datatype_map = {}
        for transactional_payload, payload_attributes in transactional_payloads.items():
            if payload_attributes.get("type"):
                transactional_payload_datatype_map[
                    transactional_payload
                ] = payload_attributes.get("type")
            else:
                raise Exception(f"{transactional_payload}, data type missing")
        return transactional_payload_datatype_map


if __name__ == "__main__":
    metadata_file = load_metadata_file("source_metadata/transactions_v1.json")
    metadata = Metadata(metadata_file).get_versioned_source_name()
