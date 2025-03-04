package components

import (
	"html/template"

	"akingbee/web/pages"
)

var _ = template.Must(pages.HtmlPage.ParseFS(templatesFS, "templates/button.html"))

type Button struct {
	Label   string
	Type    string
	FormID  string
	Icon    string
	URL     string
	Method  string
	PushURL bool
}
