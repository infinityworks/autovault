from pathlib import Path

from generate_raw_vault.app.load_metadata import get_business_topics, load_metadata_file

TEST_DATA_FILE = Path(__file__).parent.parent / "source_metadata" / "customers.json"

TEST_DATA = load_metadata_file(TEST_DATA_FILE)

def test_get_business_topics():
    topics = get_business_topics(TEST_DATA)
    assert topics

def test_get_hubs_from_business_topics():
    pass

def test_get_sats_from_hub():
    pass