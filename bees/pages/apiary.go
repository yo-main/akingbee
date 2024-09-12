package pages

import (
	"akingbee/web/components"
	"akingbee/web/pages"
	"bytes"
	"html/template"
	"log"
	"net/http"
)

var apiaryPageTemplate = template.Must(pages.HtmlPage.ParseFiles("bees/pages/templates/apiary.html"))

func HandleGetApiary(response http.ResponseWriter, req *http.Request) {
	menu, err := components.GetLoggedInMenu()
	if err != nil {
		return
	}

	var apiaryPage bytes.Buffer
	err = pages.HtmlPage.ExecuteTemplate(&apiaryPage, "apiary.html", nil)

	if err != nil {
		log.Printf("Failed to build login page: %s", err)
		return
	}

	page, err := pages.BuildPage(pages.GetBody(template.HTML(apiaryPage.Bytes()), menu))

	response.Write([]byte(page))

}
