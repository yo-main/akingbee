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

type apiaryPageParameter struct {
	Table components.Table
}

func HandleGetApiary(response http.ResponseWriter, req *http.Request) {
	menu, err := components.GetLoggedInMenu()
	if err != nil {
		return
	}

	params := apiaryPageParameter{
		Table: components.Table{
			IsBordered:  false,
			IsStripped:  true,
			IsFullWidth: true,
			Headers: []components.Header{
				{Label: "Nom"},
				{Label: "Lieu"},
				{Label: "Type de miel"},
				{Label: "Nombre de ruches"},
			},
			Rows: []components.Rows{
				{Values: []string{"Ma rucher", "Paris", "Noix", "10"}},
				{Values: []string{"Mon autre rucher", "Ganges", "Tournesol", "5"}},
				{Values: []string{"Mon beau rucher", "Puteaux", "Fleur", "8"}},
			},
		}}

	var apiaryPage bytes.Buffer
	err = pages.HtmlPage.ExecuteTemplate(&apiaryPage, "apiary.html", params)

	if err != nil {
		log.Printf("Failed to build login page: %s", err)
		return
	}

	page, err := pages.BuildPage(pages.GetBody(template.HTML(apiaryPage.Bytes()), menu))

	response.Write([]byte(page))

}
