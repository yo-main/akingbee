package components

import (
	"akingbee/web/pages"
	"html/template"
)

var tableTemplate = template.Must(pages.HtmlPage.ParseFiles("web/components/templates/table.html"))

type Table struct {
	Headers     []Header
	Rows        []Rows
	IsBordered  bool
	IsStripped  bool
	IsFullWidth bool
}

type Header struct {
	Label string
}

type Rows struct {
	Values []string
}
