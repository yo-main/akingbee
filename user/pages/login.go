package pages

import (
	"akingbee/web/components"
	"akingbee/web/pages"
	"bytes"
	"html/template"
	"log"
	"net/http"
)

var loginPageTemplate = template.Must(pages.HtmlPage.ParseFiles("user/pages/templates/login.html"))

type LoginPageBuilder struct {
	Form components.Form
}

func (data *LoginPageBuilder) Build() (template.HTML, error) {
	var loginPage bytes.Buffer
	err := pages.HtmlPage.ExecuteTemplate(&loginPage, "login.html", data)

	if err != nil {
		log.Printf("Failed to build login page: %s", err)
		return "", err
	}

	return template.HTML(loginPage.Bytes()), nil

}

func HandleGetLogin(response http.ResponseWriter, req *http.Request) {
	menu, err := components.GetLoggedOutMenu()
	if err != nil {
		return
	}

	loginParams := LoginPageBuilder{
		Form: components.Form{
			Id:     "login",
			Method: "post",
			Target: "/login",
			Swap:   "none",
			SubmitButton: components.Button{
				Label: "Se connecter",
			},
			Inputs: []components.Input{
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

	loginPage, err := loginParams.Build()
	if err != nil {
		return
	}

	page, err := pages.BuildPage(pages.GetBody(loginPage, menu))

	response.Write([]byte(page))
}

func HandleWelcomePage(response http.ResponseWriter, req *http.Request) {
	http.Redirect(response, req, "/login", http.StatusMovedPermanently)
}
