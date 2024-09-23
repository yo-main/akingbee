package components

import (
	"akingbee/web/pages"
	"html/template"
)

var formTemplate = template.Must(pages.HtmlPage.ParseFiles("web/components/templates/form.html"))
var inputTemplate = template.Must(pages.HtmlPage.ParseFiles("web/components/templates/input.html"))

type Form struct {
	Id     string
	Method string
	Target string
	Swap   string
	Inputs []Input
}

type Input struct {
	Name     string
	Label    string
	Type     string
	Required bool
	Choices  []string
	Default  string
}
