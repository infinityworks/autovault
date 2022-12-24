import itertools
from generate_raw_vault.app.find_metadata_files import load_metadata_file


class Metadata:
    def __init__(self, metadata):
        self.metadata = metadata

    def get_source_name(self):
        return self.metadata.get("source_name").replace("-", "_")

    def get_source_version(self):
        return self.metadata.get("version")

    def get_versioned_source_name(self):
        source_name = self.get_source_name()
        version = "".join(["V", self.get_source_version()])
        versioned_source_name = "_".join([source_name, version])
        return versioned_source_name

    def get_versioned_source_name_desc(self):
        return f"{self.get_versioned_source_name()}_table_desc".lower()

    def get_unit_of_work(self):
        unit_of_work = self.metadata.get("unit_of_work").replace("-", "_")
        return unit_of_work

    def get_source_system(self):
        return self.metadata.get("source_system").replace("-", "_")

    def get_target_schema(self):
        return self.metadata.get("destination_schema").replace("-", "_")

    def get_target_database(self):
        return self.metadata.get("destination_database").replace("-", "_")

    def get_table_description(self):
        return self.metadata.get("table_description")

    def get_freshness(self):
        return self.metadata.get("freshness")

    def get_file_format(self):
        return self.metadata.get("format")

    def get_filetype(self):
        return self.metadata.get("filetype")

    def get_source_location(self):
        return self.metadata.get("source_location")

    def get_access_roles(self):
        access_role_list = self.metadata.get("access_roles")
        if access_role_list:
            access_roles = ", ".join('"{0}"'.format(role) for role in access_role_list)
            return access_roles

    def get_access_requests(self):
        return self.metadata.get("access_requests")

    def get_data_quality(self):
        return self.metadata.get("quality")

    def get_warehouse_location(self):
        return self.metadata.get("warehouse_location")

    def get_maintained_by(self):
        return self.metadata.get("maintained_by")

    def get_driving_key(self):
        return self.metadata.get("driving_key")

    def get_business_topics(self):
        business_topics = self.metadata.get("business_topics")
        return business_topics

    def get_source_business_topics(self):
        topics = [topic for topic in self.get_business_topics().values()]
        return topics

    def get_hubs_from_business_topics(self):
        business_topics = self.get_business_topics()
        list_business_topics = list(business_topics.keys())
        return list_business_topics

    def check_ignore_source_from_hub_model(self, hub_name):
        business_topics = self.get_business_topics()
        hub_descriptors = business_topics.get(hub_name)
        discard_source_from_hub_model = hub_descriptors.get(
            "ignore_persisting_source_to_hub_model"
        )
        return discard_source_from_hub_model

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

    def get_key_attributes(self, hub_name):
        key_attributes = self.get_business_keys().get(hub_name)
        for attribute in key_attributes.values():
            for parameters in attribute.values():
                return parameters

    def get_topic_key(self, topic, business_topics):
        topic_key = {"business_keys": business_topics.get(topic).get("business_keys")}
        return topic_key

    def get_key_alias_map(self, hub_business_keys):
        key_alias_map = {}
        for _key, _key_attributes in hub_business_keys.get("business_keys").items():
            if _key_attributes.get("alias"):
                key_alias_map[_key] = _key_attributes.get("alias")
            else:
                key_alias_map[_key] = _key
        return key_alias_map

    def get_alias_key_map(self, key_alias_map):
        alias_key_map = {alias: _key for _key, alias in key_alias_map.items()}
        return alias_key_map

    def get_key_datatype_map(self, hub_business_keys):
        key_datatype_map = {}
        for _key, _key_attributes in hub_business_keys.get("business_keys").items():
            if _key_attributes.get("type"):
                key_datatype_map[_key] = _key_attributes.get("type")
            else:
                raise Exception(f"{_key}, data type missing")
        return key_datatype_map

    def get_key_description_map(self, hub_business_keys):
        key_attributes_map = {}
        for _key, _key_attributes in hub_business_keys.get("business_keys").items():
            if _key_attributes.get("description"):
                key_attributes_map[_key] = _key_attributes.get("description")
            else:
                raise Exception(f"{_key}, description missing")
        return key_attributes_map

    def get_hub_business_key(self, hub_name):
        hub_business_keys = self.get_business_keys().get(hub_name)
        return self.get_key_alias_map(hub_business_keys)

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

    def get_key_tests_map(self, hub_business_keys):
        key_tests_map = {}
        for _key, _key_attributes in hub_business_keys.get("business_keys").items():
            if _key_attributes.get("tests"):
                key_tests_map = _key_attributes.get("tests")
            else:
                raise Exception(f"{_key}, tests missing")
        return key_tests_map

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
