package components

import (
	"html/template"

	"akingbee/web/pages"
)

var _ = template.Must(pages.HtmlPage.ParseFS(templatesFS, "templates/update_strategy.html"))

type UpdateStrategy struct {
	Swap            string
	Target          string
	Confirm         string
	Modal           *ModalForm
	Form            *Form
	Button          *Button
	AdditionalValue string
}
