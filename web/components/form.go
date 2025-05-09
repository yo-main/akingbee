package components

import (
	"html/template"

	"akingbee/web/pages"
)

var _ = template.Must(pages.HtmlPage.ParseFS(templatesFS, "templates/form.html"))
var _ = template.Must(pages.HtmlPage.ParseFS(templatesFS, "templates/input.html"))

type Choice struct {
	Key      string
	Label    string
	Disabled bool
	Selected bool
}

type Form struct {
	ID     string
	URL    string
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
	Placeholder   string
}
