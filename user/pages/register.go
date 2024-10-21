package pages

import (
	"akingbee/internal/htmx"
	"akingbee/web"
	"akingbee/web/components"
	"akingbee/web/pages"
	"bytes"
	"html/template"
	"log"
	"net/http"
)

var registerPageTemplate = template.Must(pages.HtmlPage.ParseFS(templatesFS, "templates/register.html"))

type registerPageParams struct {
	SubmitButton components.Button
	Form         components.UpdateStrategy
}

func HandleGetRegister(response http.ResponseWriter, req *http.Request) {
	params := registerPageParams{
		SubmitButton: components.Button{
			Label:  "S'enregistrer",
			FormId: "post-user",
			Type:   "is-link",
		},
		Form: components.UpdateStrategy{
			Target: "#page-body",
			Swap:   "innerHTML",
			Form: &components.Form{
				Id:     "post-user",
				Url:    "/users",
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

	if htmx.IsHtmxRequest(req) {
		response.Write(registerPage.Bytes())
	} else {
		web.ReturnFullPage(req.Context(), req, response, *&registerPage, nil)
	}
}
