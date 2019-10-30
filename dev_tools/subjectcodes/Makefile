SHELL=bash

BUILD=build
BUILD_ARCH=$(BUILD)/$(GOOS)-$(GOARCH)
BIN_DIR?='mongo'

export GOOS?=$(shell go env GOOS)
export GOARCH?=$(shell go env GOARCH)

build:
	@mkdir -p $(BUILD_ARCH)/$(BIN_DIR)
	go build -o $(BUILD_ARCH)/$(BIN_DIR) main.go
debug:
	HUMAN_LOG=1 go run main.go

.PHONEY: build debug
