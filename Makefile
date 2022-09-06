mac_setup:
	dbt deps
	python3 -m pip install --upgrade pip
	python3 -m venv .venv
	source .venv/bin/activate && pip3 install --requirement requirements.txt

docs:
	dbt docs generate && dbt docs serve

autovault:
	export PYTHONPATH="${PYTHONPATH}:${pwd}" && source .venv/bin/activate && python3 generate_raw_vault/app/main.py
