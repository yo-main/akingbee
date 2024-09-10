package login

import (
	"akingbee/app/core/api/templates"
	"bytes"
	"html/template"
	"log"
	"net/http"
)

var loginPageTemplate = template.Must(templates.HtmlPage.ParseFiles("front/pages/login.html"))

type loginPageParams struct {
	Form templates.Form
}

func HandleGetLogin(response http.ResponseWriter, req *http.Request) {
	menu, err := templates.GetLoggedOutMenu()
	if err != nil {
		return
	}

	loginParams := loginPageParams{
		Form: templates.Form{
			Id:     "login",
			Method: "post",
			Target: "/login",
			SubmitButton: templates.Button{
				Label: "Se connecter",
				Swap:  "none",
			},
			Inputs: []templates.Input{
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
		}}

	var loginPage bytes.Buffer
	err = templates.HtmlPage.ExecuteTemplate(&loginPage, "login.html", loginParams)

	if err != nil {
		log.Printf("Failed to build login page: %s", err)
		return
	}

	page, err := templates.BuildPage(templates.GetBody(template.HTML(loginPage.Bytes()), menu))

	response.Write([]byte(page))
}

func HandleWelcomePage(response http.ResponseWriter, req *http.Request) {
	http.Redirect(response, req, "/login", http.StatusMovedPermanently)
}
