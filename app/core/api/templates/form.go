package templates

import (
	"html/template"
)

var formTemplate = template.Must(HtmlPage.ParseFiles("front/components/form.html"))
var buttonTemplate = template.Must(HtmlPage.ParseFiles("front/components/button.html"))
var inputTemplate = template.Must(HtmlPage.ParseFiles("front/components/input.html"))

type Form struct {
	Id           string
	Method       string
	Target       string
	Swap         string
	SubmitButton Button
	Inputs       []Input
}

type Button struct {
	Label string
}

type Input struct {
	Name     string
	Label    string
	Type     string
	Required bool
}
