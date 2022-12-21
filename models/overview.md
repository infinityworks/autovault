{% docs __overview__ %}
# Integrated Data Model

This project facilitates data discovery through a dictionary and lineage. Each source and model are fully described and include attributes such as:
- Description
- Role Access
- Maintainer
- Source system
  - Business process
  - Storage (lake)
- Driving key
- Required field
- Uniqueness

- Account access / database access
- Tools to access
- Slack request or form, approve, give role. How to get status of access request.
- How often we get the data
- Typical use
- Known issues
- Ongoing work
- table schema evolution
- PII
- Data structure, csv json
- glossary, domain specific language, abreviations
- modelb last updated
- information on aliased columns
- mapping tables e.g. for ID
- governance
- global to a role for hubs and links; more granular RBAC for each satellite to take presidence over global role;
## Navigation
You can use the Project and Database navigation tabs on the left side of the window to explore the models in your project.

### Project Tab
The Project tab mirrors the directory structure of the dbt project. In this tab, you can see all of the models defined in your dbt project, as well as models imported from dbt packages.

### Database Tab
The Database tab also exposes your models, but in a format that looks more like a database explorer. This view shows relations (tables and views) grouped into database schemas. Note that ephemeral models are not shown in this interface, as they do not exist in the database.

### Graph Exploration
You can click the blue icon on the bottom-right corner of the page to view the lineage graph of your models.

On model pages, you'll see the immediate parents and children of the model you're exploring. By clicking the Expand button at the top-right of this lineage pane, you'll be able to see all of the models that are used to build, or are built from, the model you're exploring.

Once expanded, you'll be able to use the --select and --exclude model selection syntax to filter the models in the graph. For more information on model selection, check out the dbt docs.

Note that you can also right-click on models to interactively filter and explore the graph.
{% enddocs %}
