package login

import (
	"akingbee/app/core/api/templates"
	"bytes"
	"html/template"
	"log"
	"net/http"
)

var registerPageTemplate = template.Must(templates.HtmlPage.ParseFiles("front/pages/register.html"))

type registerPageParams struct {
	Form templates.Form
}

func HandleGetRegister(response http.ResponseWriter, req *http.Request) {
	menu, err := templates.GetLoggedOutMenu()
	if err != nil {
		return
	}

	params := registerPageParams{
		Form: templates.Form{
			Id:     "post-user",
			Method: "post",
			Target: "/users",
			SubmitButton: templates.Button{
				Label: "S'enregistrer",
				Swap:  "none",
			},
			Inputs: []templates.Input{
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
	err = templates.HtmlPage.ExecuteTemplate(&registerPage, "register.html", params)

	if err != nil {
		log.Printf("Failed to build register page: %s", err)
		return
	}

	page, err := templates.BuildPage(templates.GetBody(template.HTML(registerPage.Bytes()), menu))

	if err != nil {
		log.Printf("Failed to build register page: %s", err)
		return
	}

	response.Write(page)
}
