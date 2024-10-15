package components

import (
	"akingbee/web/pages"
	"html/template"
)

var updateStrategyTemplate = template.Must(pages.HtmlPage.ParseFiles("web/components/templates/update_strategy.html"))

type UpdateStrategy struct {
	Swap            string
	Target          string
	Confirm         string
	Modal           *ModalForm
	Form            *Form
	Button          *Button
	AdditionalValue string
}
