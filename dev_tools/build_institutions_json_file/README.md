build_institutions_json_file
=================
Script to create an institutions.json file from the ukprn_name, which is read from the ukrlp CosmosDB container.

### Configuration Settings

Before running the script, set the following environment variables.

| Variable                            | Default                | Description                                              |
| ----------------------------------- | ---------------------- | -------------------------------------------------------- |
| AzureCosmosDbDatabaseId | retrieve from portal | The id of a CosmosDB instance that holds the latest ukrlp data in a container called urkrlp.|
| AzureCosmosDbUkRlpCollectionId | ukrlp | the container name holding the ukrlp data |
| AzureCosmosDbUri | retrieve from portal | the uri to CosmosDB |
| AzureCosmosDbKey | retrieve from portal | the key to authenticate to CosmosDB |


### Setup

* Ensure python 3.6.8 is installed
* Create a Python virtualenv to run this tool in
* Activate the virtualenv

```
pip install -r requirements.txt
```

### Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for details.

### License

See [LICENSE](LICENSE.md) for details.