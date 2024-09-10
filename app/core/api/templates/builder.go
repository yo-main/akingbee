package templates

import (
	"bytes"
	"fmt"
	"html/template"
	"log"
)

type htmlBodyComponent struct {
	Menu    template.HTML
	Content template.HTML
}

type htmlPageComponent struct {
	Body htmlBodyComponent
}

var HtmlPage = template.Must(template.ParseFiles("front/pages/index.html"))
var htmlBody = template.Must(HtmlPage.ParseFiles("front/pages/body.html"))

func BuildPage(body htmlBodyComponent) ([]byte, error) {

	params := htmlPageComponent{
		Body: body,
	}

	var buffer bytes.Buffer
	err := HtmlPage.Execute(&buffer, params)
	if err != nil {
		log.Printf("Error while building html page: %s", err)
	}

	return buffer.Bytes(), nil

}

func GetBody(content template.HTML, menu template.HTML) htmlBodyComponent {
	return htmlBodyComponent{
		Menu:    menu,
		Content: content,
	}
}

func BuildSuccessNotification(content string) template.HTML {
	return template.HTML(fmt.Sprintf(`
	<div class="notification is-success">
		<button class="delete" hx-get="data:text/html," hx-target="closest .notification" hx-swap="delete"></button>
		<div>%s</div>
	</div>
	`, content))
}

func BuildErrorNotification(content string) template.HTML {
	return template.HTML(fmt.Sprintf(`
	<div class="notification is-danger">
		<button class="delete" hx-get="data:text/html," hx-target="closest .notification" hx-swap="delete"></button>
		<div>%s</div>
	</div>
	`, content))
}
