package pages

import (
	"akingbee/bees/repositories"
	"akingbee/user/services"
	"akingbee/web/components"
	"akingbee/web/pages"
	"bytes"
	"html/template"
	"log"
	"net/http"
	"strconv"
)

var apiaryPageTemplate = template.Must(pages.HtmlPage.ParseFiles("bees/pages/templates/apiary.html"))

type apiaryPageParameter struct {
	CreateApiaryModal components.ModalForm
	Table             components.Table
}

func HandleGetApiary(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()

	userId, err := services.AuthenticateUser(req)

	if err != nil {
		log.Printf("Could not authenticate user: %s", err)
		response.WriteHeader(http.StatusUnauthorized)
		return
	}

	menu, err := components.GetLoggedInMenu()
	if err != nil {
		log.Printf("Could not get logged in menu: %s", err)
		return
	}

	apiaries, err := repositories.GetApiary(ctx, userId)
	if err != nil {
		log.Printf("Could not get apiaries: %s", err)
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	rows := []components.Rows{}
	for _, apiary := range apiaries {
		rows = append(rows, components.Rows{
			Values: []string{apiary.Name, apiary.Location, apiary.HoneyKind, strconv.Itoa(apiary.HiveCount)},
		})

	}

	params := apiaryPageParameter{
		CreateApiaryModal: components.ModalForm{
			Title:       "Création un nouveau rucher",
			ButtonLabel: "Nouveau rucher",
			Form: components.Form{
				Id:     "createApiary",
				Method: "post",
				Target: "/apiary",
				Swap:   "none",
				Inputs: []components.Input{
					{
						Name:     "name",
						Label:    "Nom",
						Type:     "text",
						Required: true,
					},
					{
						Name:     "location",
						Label:    "Location",
						Type:     "text",
						Required: true,
					},
					{
						Name:     "honeyKind",
						Label:    "Type de miel",
						Type:     "text",
						Required: true,
					},
				},
				SubmitButton: components.Button{
					Label:  "Créer",
					Type:   "is-link",
					FormId: "createApiary",
				},
			}},
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
			Rows: rows,
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
