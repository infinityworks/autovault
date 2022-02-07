from generate_raw_vault.app.find_metadata_files import load_metadata_file
from generate_raw_vault.tests.conftest import METADATA_TESTFILE_PATH
from json import loads
import pytest


def test_load_metadata_file():
    test_file = load_metadata_file(METADATA_TESTFILE_PATH)
    test_json = """{
	"business_topics": {
		"HUB1": {
			"business_attributes": [{
					"business_definition": "SAT1",
					"payload": {
						"sat1_col1": "STRING",
						"sat1_col2": "STRING"
					}
				},
				{
					"business_definition": "SAT2",
					"payload": {
						"sat2_col1": "STRING"
					}
				}
			],
			"business_keys": {
				"pk1": {
					"alias": "pk1",
					"type": "STRING"
				}
			}
		},
		"HUB2": {
			"business_attributes": [{
				"business_definition": "SAT3",
				"payload": {
					"sat3_col1": "STRING"
				}
			}],
			"business_keys": {
				"pk2": {
					"type": "STRING"
				}
			}
		}

	},
	"destination_database": "AUTOVAULT",
	"destination_schema": "PUBLIC",
	"source_name": "TEST",
	"source_system": "CSV",
	"unit_of_work": "TEST_UoW",
	"version": "1"
}"""
    assert test_file == loads(test_json)
