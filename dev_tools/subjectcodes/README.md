get-list-of-institutions
==================
A script to read list of subject codes from a csv file and generate en equivalent a json file.

### Installation

As the script is written in Go, make sure you have version 1.10.0 or greater installed.

Using [Homebrew](https://brew.sh/) to install go
* Run `brew install go` or `brew upgrade go`
* Set your `GOPATH` environment variable, this specifies the location of your workspace

#### Running script

* Run `make debug`

### JSON output

```json
[
  {
    "code": "string",
    "english_name": "string",
    "welsh_name": "string",
    "level": "string"
  },
  ...
]
```

### Contributing

See [CONTRIBUTING](../CONTRIBUTING.md) for details.

### License

See [LICENSE](../LICENSE.md) for details.
