package pages

import (
	"akingbee/internal/htmx"
	"akingbee/user/services"
	"akingbee/web/components"
	"akingbee/web/pages"
	"bytes"
	"html/template"
	"log"
	"net/http"
)

var loginPageTemplate = template.Must(pages.HtmlPage.ParseFiles("user/pages/templates/login.html"))

type LoginPageBuilder struct {
	Form         components.Form
	SubmitButton components.Button
}

func (data *LoginPageBuilder) Build() (*bytes.Buffer, error) {
	var loginPage bytes.Buffer
	err := pages.HtmlPage.ExecuteTemplate(&loginPage, "login.html", data)

	if err != nil {
		log.Printf("Failed to build login page: %s", err)
		return nil, err
	}

	return &loginPage, nil

}

func HandleGetLogin(response http.ResponseWriter, req *http.Request) {
	loginParams := LoginPageBuilder{
		SubmitButton: components.Button{
			Label:  "Se connecter",
			Type:   "is-link",
			FormId: "login",
		},
		Form: components.Form{
			Id:     "login",
			Method: "post",
			Target: "/login",
			Swap:   "none",
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
		log.Printf("Could not load login page: %s", err)
		return
	}

	if htmx.IsHtmxRequest(req) {
		response.Write(loginPage.Bytes())
	} else {
		menu, err := components.GetLoggedOutMenu()
		if err != nil {
			log.Printf("Could not build logged out menu: %s", err)
			return
		}

		page, err := pages.BuildPage(pages.GetBody(template.HTML(loginPage.Bytes()), template.HTML(menu.Bytes())))

		response.Write([]byte(page))
	}
}

func GetWelcomePage(req *http.Request) (*bytes.Buffer, error) {

	var page bytes.Buffer
	page.WriteString("COUCOU")
	return &page, nil
}

func HandleWelcomePage(response http.ResponseWriter, req *http.Request) {
	welcomePage, err := GetWelcomePage(req)

	if err != nil {
		log.Printf("Could not get welcome page content: %s", err)
		return
	}

	if htmx.IsHtmxRequest(req) {
		response.Write([]byte(welcomePage.Bytes()))
	} else {
		_, err = services.AuthenticateUser(req)

		var menu *bytes.Buffer

		if err != nil {
			menu, err = components.GetLoggedOutMenu()
		} else {
			menu, err = components.GetLoggedInMenu()
		}

		page, err := pages.BuildPage(pages.GetBody(template.HTML(welcomePage.Bytes()), template.HTML(menu.Bytes())))
		if err != nil {
			log.Printf("Could not build welcome page content: %s", err)
			return
		}
		response.Write([]byte(page))
	}
}
