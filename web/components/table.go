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

type Value struct {
	Label     string
	ModalForm ModalForm
}

type Rows struct {
	Values []Value
}
