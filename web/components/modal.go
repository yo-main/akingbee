package components

import (
	"akingbee/web/pages"
	"html/template"
)

var modalTemplate = template.Must(pages.HtmlPage.ParseFS(templatesFS, "templates/modal.html"))

type ModalForm struct {
	Title            string
	ShowModalButton  Button
	SubmitFormButton Button
	Form             Form
}
