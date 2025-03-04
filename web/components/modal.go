package components

import (
	"html/template"

	"akingbee/web/pages"
)

var _ = template.Must(pages.HtmlPage.ParseFS(templatesFS, "templates/modal.html"))

type ModalForm struct {
	Title            string
	ShowModalButton  Button
	SubmitFormButton Button
	Form             Form
}
