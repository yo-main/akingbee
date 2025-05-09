package pages

import (
	"bytes"
	"html/template"
	"log"
	"net/http"

	api_helpers "akingbee/internal/web"
	"akingbee/web/components"
	"akingbee/web/pages"
)

var _ = template.Must(pages.HtmlPage.ParseFS(templatesFS, "templates/register.html"))

type registerPageParams struct {
	SubmitButton components.Button
	Form         components.UpdateStrategy
}

func HandleGetRegister(response http.ResponseWriter, req *http.Request) {
	params := registerPageParams{
		SubmitButton: components.Button{
			Label:  "S'enregistrer",
			FormID: "post-user",
			Type:   "is-link",
		},
		Form: components.UpdateStrategy{
			Target: "#page-body",
			Swap:   "innerHTML",
			Form: &components.Form{
				ID:     "post-user",
				URL:    "/users",
				Method: "post",
				Inputs: []components.Input{
					{
						Name:     "email",
						Label:    "Email",
						Type:     "email",
						Required: true,
					},
					{
						Name:     "username",
						Label:    "Identifiant",
						Type:     "text",
						Required: true,
					},
					{
						Name:     "password",
						Label:    "Mot de passe",
						Type:     "password",
						Required: true,
					},
				},
			},
		},
	}

	var registerPage bytes.Buffer
	err := pages.HtmlPage.ExecuteTemplate(&registerPage, "register.html", params)

	if err != nil {
		log.Printf("Failed to build register page: %s", err)
		return
	}

	api_helpers.WriteToResponse(response, registerPage.Bytes())
}
