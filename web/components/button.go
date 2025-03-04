package components

import (
	"akingbee/web/pages"
	"html/template"
)

var buttonTemplate = template.Must(pages.HtmlPage.ParseFS(templatesFS, "templates/button.html"))

type Button struct {
	Label   string
	Type    string
	FormID  string
	Icon    string
	URL     string
	Method  string
	PushURL bool
}
