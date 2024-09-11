package templates

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

type NotificationComponent struct {
	Type    string
	Content string
}

var HtmlPage = template.Must(template.ParseFiles("front/pages/index.html"))
var htmlBody = template.Must(HtmlPage.ParseFiles("front/pages/body.html"))
var notificationComponent = template.Must(HtmlPage.ParseFiles("front/components/notification.html"))

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

func (data *NotificationComponent) Build() (template.HTML, error) {
	var buffer bytes.Buffer
	err := HtmlPage.ExecuteTemplate(&buffer, "notification.html", data)
	if err != nil {
		log.Printf("Error while building notification: %s", err)
	}

	return template.HTML(buffer.Bytes()), nil
}
