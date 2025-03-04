package pages

import (
	"bytes"
	"embed"
	"html/template"
	"log"
	"net/http"

	api_helpers "akingbee/internal/web"
	"akingbee/web/components"
	"akingbee/web/pages"
)

//go:embed templates/*
var templatesFS embed.FS

var loginPageTemplate = template.Must(pages.HtmlPage.ParseFS(templatesFS, "templates/login.html"))

type LoginPageBuilder struct {
	Form                 components.UpdateStrategy
	SubmitButton         components.Button
	ForgotPasswordButton components.Button
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

func GetLoginPage() (*bytes.Buffer, error) {
	loginParams := LoginPageBuilder{
		SubmitButton: components.Button{
			Label:  "Se connecter",
			Type:   "is-link",
			FormID: "login",
		},
		Form: components.UpdateStrategy{
			Target: "#page-body",
			Swap:   "innerHTML",
			Form: &components.Form{
				ID:     "login",
				Method: "post",
				URL:    "/login",
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
			},
		},
		ForgotPasswordButton: components.Button{
			Label:   "Mot de passe oublié",
			URL:     "password-reset",
			PushURL: true,
			Method:  "get",
		},
	}

	loginPage, err := loginParams.Build()
	return loginPage, err
}

func HandleGetLogin(response http.ResponseWriter, req *http.Request) {
	loginPage, err := GetLoginPage()
	if err != nil {
		log.Printf("Could not build login page: %s", err)
		return
	}

	api_helpers.WriteToResponse(response, loginPage.Bytes())
}

func GetWelcomePage(req *http.Request) (*bytes.Buffer, error) {
	var page bytes.Buffer
	return &page, nil
}

func HandleWelcomePage(response http.ResponseWriter, req *http.Request) {
	welcomePage, err := GetWelcomePage(req)

	if err != nil {
		log.Printf("Could not get welcome page content: %s", err)
		return
	}

	api_helpers.WriteToResponse(response, []byte(welcomePage.Bytes()))
}
