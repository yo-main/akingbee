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

var registerPageTemplate = template.Must(pages.HtmlPage.ParseFiles("user/pages/templates/register.html"))

type registerPageParams struct {
	SubmitButton components.Button
	Form         components.Form
}

func HandleGetRegister(response http.ResponseWriter, req *http.Request) {
	params := registerPageParams{
		SubmitButton: components.Button{
			Label:  "S'enregistrer",
			FormId: "post-user",
			Type:   "is-link",
		},
		Form: components.Form{
			Id:     "post-user",
			Method: "post",
			Url:    "/users",
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
		web.ReturnFullPage(req.Context(), response, *&registerPage, nil)
	}
}
