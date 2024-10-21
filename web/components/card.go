package components

import (
	"akingbee/web/pages"
	"bytes"
	"html/template"
	"log"
)

var cardTemplate = template.Must(pages.HtmlPage.ParseFS(templatesFS, "templates/card.html"))

type Card struct {
	Id      string
	Header  CardHeader
	Content CardContent
	Footer  CardFooter
}

func (card *Card) Build() (*bytes.Buffer, error) {
	var content bytes.Buffer
	err := pages.HtmlPage.ExecuteTemplate(&content, "card.html", card)

	if err != nil {
		log.Printf("Failed to build card: %s", err)
		return nil, err
	}

	return &content, nil
}

type CardHeader struct {
	Title  string
	Button Button
}

type CardFooterItem struct {
	UpdateStrategy *UpdateStrategy
}

type CardFooter struct {
	Items []CardFooterItem
}

type CardContent struct {
	Id              string
	HorizontalTable HorizontalTable
}

type HorizontalTable struct {
	Values []HorizontalTableValue
}

type HorizontalTableValue struct {
	Key   string
	Value string
}
