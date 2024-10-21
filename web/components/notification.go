package components

import (
	"akingbee/web/pages"
	"bytes"
	"html/template"
	"log"
)

var notificationComponent = template.Must(pages.HtmlPage.ParseFS(templatesFS, "templates/notification.html"))

type NotificationComponent struct {
	Type    string
	Content string
}

func (data *NotificationComponent) Build() (template.HTML, error) {
	var buffer bytes.Buffer
	err := pages.HtmlPage.ExecuteTemplate(&buffer, "notification.html", data)
	if err != nil {
		log.Printf("Error while building notification: %s", err)
	}

	return template.HTML(buffer.Bytes()), nil
}
