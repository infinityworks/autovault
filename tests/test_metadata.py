from pathlib import Path
from generate_raw_vault.app.metadata import BusinessTopic, Metadata, load_metadata

TEST_DATA_FILE = Path(__file__).parent.parent / "source_metadata" / "customers.json"


def test_load_metadata():
    meta: Metadata = load_metadata(TEST_DATA_FILE)
    assert meta.source_name == "CUSTOMERS"
    assert len(meta.business_topics) == 2
    assert meta.business_topics["CUSTOMER"].business_keys == {"CUSTOMER_ID": "STRING"}

    meta.satelites()
