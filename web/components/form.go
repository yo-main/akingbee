package components

import (
	"akingbee/web/pages"
	"html/template"
)

var formTemplate = template.Must(pages.HtmlPage.ParseFiles("web/components/templates/form.html"))
var inputTemplate = template.Must(pages.HtmlPage.ParseFiles("web/components/templates/input.html"))

type Choice struct {
	Key      string
	Label    string
	Disabled bool
	Selected bool
}

type Form struct {
	Id     string
	Url    string
	Method string
	Inputs []Input
}

type Input struct {
	Name          string
	Label         string
	Type          string
	Required      bool
	ChoicesFree   []Choice
	ChoicesStrict []Choice
	Default       string
	DefaultHTML   template.HTML
	RichEditor    bool
	GroupedInput  []Input
	Narrow        bool
	Hidden        bool
}
