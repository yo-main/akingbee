package components

import (
	"akingbee/web/pages"
	"bytes"
	"html/template"
	"log"
)

var tableTemplate = template.Must(pages.HtmlPage.ParseFiles("web/components/templates/table.html"))
var tableRowTemplate = template.Must(pages.HtmlPage.ParseFiles("web/components/templates/table_row.html"))
var tableCellTemplate = template.Must(pages.HtmlPage.ParseFiles("web/components/templates/table_cell.html"))

type Table struct {
	Headers     []Header
	Rows        []Row
	IsBordered  bool
	IsStripped  bool
	IsFullWidth bool
}

type Header struct {
	Label string
}

type Cell struct {
	Label     string
	UpdateRow bool
	ModalForm ModalForm
}

type Row struct {
	Cells []Cell
}

func (row *Row) Build() (*bytes.Buffer, error) {
	var content bytes.Buffer
	err := pages.HtmlPage.ExecuteTemplate(&content, "table_row.html", row)

	if err != nil {
		log.Printf("Failed to build table cell: %s", err)
		return nil, err
	}

	return &content, nil

}
