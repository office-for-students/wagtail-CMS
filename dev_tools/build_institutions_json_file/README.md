build_institutions_json_file
=================
Script to create an institutions.json file from the ukprn_name, which is read from the institutions CosmosDB container.

### Configuration Settings

Before running the script, set the following environment variables.

| Variable                              | Default                | Description                                              |
| ------------------------------------- | ---------------------- | -------------------------------------------------------- |
| AzureCosmosDbDatabaseId               | retrieve from portal | The id of a CosmosDB instance that holds the latest ukrlp data in a container called urkrlp.|
| AzureCosmosDbInstitutionsCollectionId | ukrlp | the container name holding the institution data |
| AzureCosmosDbUri                      | retrieve from portal | the uri to CosmosDB |
| AzureCosmosDbKey                      | retrieve from portal | the key to authenticate to CosmosDB |
| Version                               | Check latest version of institutions.json file | The version number, bumped from the existing institution list |
| InstitutionVersion                    | Check latest successful version of dataset doc | The institution version number should be the latest successful version of a dataset resource in cosmos db |


### Setup

* Ensure python 3.6.8 is installed
* Create a Python virtualenv to run this tool in
* Activate the virtualenv

```
pip install -r requirements.txt
```
