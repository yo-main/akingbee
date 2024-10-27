package pages

import (
	"bytes"
	"embed"
	"html/template"
	"log"
)

//go:embed templates/*

var templatesFS embed.FS

var notFoundBody = template.Must(template.ParseFS(templatesFS, "templates/404.html"))

func GetNotFoundContent() *bytes.Buffer {
	var body bytes.Buffer

	err := notFoundBody.Execute(&body, nil)
	if err != nil {
		log.Printf("Could not build 404 page: %s", err)
	}

	return &body
}
