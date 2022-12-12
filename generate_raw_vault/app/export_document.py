from pathlib import Path

from generate_raw_vault.app.find_metadata_files import load_metadata_file
from generate_raw_vault.app.find_metadata_files import load_template
from generate_raw_vault.app.metadata_handler import Metadata

class ExportDocument(Metadata):
    
    def __init__(self, metadata, template):
        self.metadata = metadata
        self.template = template
        
    def get_versioned_source_name_desc(self):
        versioned_source_name = self.get_versioned_source_name().lower()
        versioned_source_name_desc = "".join([versioned_source_name,"_desc"])
        return versioned_source_name_desc
        
    def get_table_description(self):
        table_description = self.metadata.get("table_description")
        return table_description
        
    def get_freshness(self):
        freshness = self.metadata.get("freshness")
        return freshness
        
    def get_format(self):
        format = self.metadata.get("format")
        return format
        
    def get_filetype(self):
        filetype = self.metadata.get("filetype")
        return filetype
    
    def get_source_location(self):
        source_location = self.metadata.get("source_location")
        return source_location
    
    def get_database_location(self):
        database_location = self.metadata.get("database_location")
        return database_location
        
    def get_access_roles(self):
        access_roles = self.metadata.get("access_roles")
        access_roles = ', '.join('"{0}"'.format(role) for role in access_roles)
        return access_roles
    
    def get_access_requests(self):
        access_requests = self.metadata.get("access_requests")
        return access_requests
        
    def get_version(self):
        version = self.metadata.get("version")
        return version
        
    def get_quality(self):
        quality = self.metadata.get("quality")
        return quality
        
    
    def safe_substitute(self):
        substitute_metadata = self.template.safe_substitute(
                                versioned_source_name_desc = self.get_versioned_source_name_desc(),
                                versioned_source_name = self.get_versioned_source_name(),
                                table_description = self.get_table_description(),
                                unit_of_work = self.get_unit_of_work(),
                                source_name = self.get_source_name(),
                                version = self.get_version(),
                                freshness = self.get_freshness(),
                                format = self.get_format(),
                                filetype = self.get_filetype(),
                                source_location = self.get_source_location(),
                                database_location = self.get_database_location(),
                                access_roles = self.get_access_roles(),
                                access_requests = self.get_access_requests(),
                                quality = self.get_quality()
                             )
        return substitute_metadata
    
    def create_document(self, file_path):
        substitute_metadata = self.safe_substitute()
        with open(
            Path(f"./{file_path}"), "w"
        ) as doc:
            doc.write(substitute_metadata)
        
if __name__ == "__main__":
    template = load_template("generate_raw_vault/app/templates/documentation.md")
    metadata_file = load_metadata_file("source_metadata/customers_v0_1_1.json")
    doc_exporter = ExportDocument(metadata_file,template)
    doc_exporter.create_document("models/source_descriptions/customers_v0_1_0.md")