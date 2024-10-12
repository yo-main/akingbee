package components

import (
	"akingbee/web/pages"
	"html/template"
)

var cardTemplate = template.Must(pages.HtmlPage.ParseFiles("web/components/templates/card.html"))

type Card struct {
	Header  CardHeader
	Content CardContent
	Footer  CardFooter
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
