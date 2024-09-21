package components

import (
	"akingbee/web/pages"
	"html/template"
)

var modalTemplate = template.Must(pages.HtmlPage.ParseFiles("web/components/templates/modal.html"))

type ModalForm struct {
	Title                 string
	ShowModalButtonLabel  string
	SubmitFormButtonLabel string
	Form                  Form
}
