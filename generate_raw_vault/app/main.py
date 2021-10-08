import json
import itertools
from generate_raw_vault.app.export_ddl_statement import export_all_ddl_statments


def main():
    export_all_ddl_statments()
    # create_stages()
    # create_hubs()
    # create_sats()
    # create_links()


if __name__ == "__main__":
    main()
