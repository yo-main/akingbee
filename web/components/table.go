package components

import (
	"akingbee/web/pages"
	"bytes"
	"html/template"
	"log"
)

var tableTemplate = template.Must(pages.HtmlPage.ParseFS(templatesFS, "templates/table.html"))
var tableRowTemplate = template.Must(pages.HtmlPage.ParseFS(templatesFS, "templates/table_row.html"))
var tableCellTemplate = template.Must(pages.HtmlPage.ParseFS(templatesFS, "templates/table_cell.html"))

type Table struct {
	Id          string
	ColumnSizes []ColumnSize
	Headers     []Header
	Rows        []Row
	IsBordered  bool
	IsStripped  bool
	IsFullWidth bool
}

func (table *Table) Build() (*bytes.Buffer, error) {
	var content bytes.Buffer
	err := pages.HtmlPage.ExecuteTemplate(&content, "table.html", table)

	if err != nil {
		log.Printf("Failed to build table: %s", err)
		return nil, err
	}

	return &content, nil

}

type Header struct {
	Label string
}

type ColumnSize struct {
	Span  string
	Style string
}

type Cell struct {
	Label          string
	HTMLContent    template.HTML
	UpdateStrategy *UpdateStrategy
	GroupedCells   []Cell
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
