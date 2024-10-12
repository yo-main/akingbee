package components

import (
	"akingbee/web/pages"
	"html/template"
)

var buttonTemplate = template.Must(pages.HtmlPage.ParseFiles("web/components/templates/button.html"))

type Button struct {
	Label   string
	Type    string
	FormId  string
	Icon    string
	Url     string
	Method  string
	PushUrl bool
}
