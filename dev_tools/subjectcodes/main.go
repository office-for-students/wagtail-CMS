package main

import (
	"bufio"
	"encoding/csv"
	"encoding/json"
	"flag"
	"io"
	"io/ioutil"
	"os"

	"github.com/ONSdigital/go-ns/log"
)

var (
	inputFilename        = "english-and-welsh-subject-names.csv"
	outputFilename       = "subject-codes.json"
	relativeFileLocation = "./"
)

func main() {
	flag.StringVar(&inputFilename, "input-filename", inputFilename, "input filename")
	flag.StringVar(&outputFilename, "output-filename", outputFilename, "output filename")
	flag.Parse()

	listOfSubjects, err := getSubjectNames(inputFilename)
	if err != nil {
		log.ErrorC("error creating list of institution names", err, nil)
		os.Exit(1)
	}

	file, err := json.MarshalIndent(listOfSubjects, "", "  ")
	if err != nil {
		log.ErrorC("error marshalling list of subjects", err, nil)
		os.Exit(1)
	}

	if err = ioutil.WriteFile(outputFilename, file, 0644); err != nil {
		log.ErrorC("error writing list of subjects to json file", err, log.Data{"filename": outputFilename})
		os.Exit(1)
	}

	log.Info("completed creation of list of subjects", nil)

}

// SubjectObject represents a document containing information on a subject
type SubjectObject struct {
	Code        string `json:"code"`
	EnglishName string `json:"english_name"`
	WelshName   string `json:"welsh_name"`
	Level       string `json:"level"`
}

func getSubjectNames(filename string) (subjectList []SubjectObject, err error) {
	csvFile, err := os.Open(relativeFileLocation + filename)
	if err != nil {
		log.ErrorC("encountered error immediately when attempting to open file", err, log.Data{"file name": filename})
		return
	}
	csvReader := csv.NewReader(bufio.NewReader(csvFile))

	// Scan header row (not needed)
	_, err = csvReader.Read()
	if err != nil {
		log.ErrorC("encountered error immediately when processing header row", err, nil)
		return
	}

	count := 0
	for {
		line, err := csvReader.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.ErrorC("encountered error reading csv", err, log.Data{"line_count": count, "csv_line": line})
			break
		}

		// name := strings.Replace(line[1], "/", ",", -1)

		subjectObject := SubjectObject{
			Code:        line[0],
			EnglishName: line[1],
			Level:       line[2],
			WelshName:   line[3],
		}

		subjectList = append(subjectList, subjectObject)

		count++
	}

	log.Info("created subject names as json resource", log.Data{"number_of_subjects": count})

	return
}
