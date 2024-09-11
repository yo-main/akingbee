package pages

import (
	"bytes"
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

var HtmlPage = template.Must(template.ParseFiles("web/pages/templates/index.html"))
var htmlBody = template.Must(HtmlPage.ParseFiles("web/pages/templates/body.html"))

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
