package components

import (
	"bytes"
	"embed"
	"html/template"
	"strings"

	"akingbee/user/models"
	"akingbee/web/pages"
)

//go:embed templates/*
var templatesFS embed.FS

type LoggedInMenuComponent struct {
	Username       string
	Entity         string
	CanImpersonate bool
}

type LoggedOutMenuComponent struct {
}

var loggedOutMenu = template.Must(pages.HtmlPage.ParseFS(templatesFS, "templates/navbar_logged_out.html"))
var loggedInMenu = template.Must(pages.HtmlPage.ParseFS(templatesFS, "templates/navbar_logged_in.html"))

func GetLoggedInMenu(user *models.AuthenticatedUser, url string) (*bytes.Buffer, error) {
	urlParts := strings.Split(url, "/")
	params := LoggedInMenuComponent{
		Username:       user.Credentials.Username,
		Entity:         urlParts[len(urlParts)-1],
		CanImpersonate: user.IsAdmin() || user.Impersonator != nil,
	}

	var buffer bytes.Buffer
	err := loggedInMenu.ExecuteTemplate(&buffer, "navbar_logged_in.html", params)

	return &buffer, err
}

func GetLoggedOutMenu() (*bytes.Buffer, error) {
	params := LoggedOutMenuComponent{}

	var buffer bytes.Buffer
	err := loggedOutMenu.ExecuteTemplate(&buffer, "navbar_logged_out.html", params)

	return &buffer, err
}
