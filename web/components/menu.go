package components

import (
	"akingbee/web/pages"
	"bytes"
	"embed"
	"html/template"
	"strings"
)

//go:embed templates/*
var templatesFS embed.FS

type LoggedInMenuComponent struct {
	Username string
	Entity   string
	IsAdmin  bool
}

type LoggedOutMenuComponent struct {
}

var loggedOutMenu = template.Must(pages.HtmlPage.ParseFS(templatesFS, "templates/navbar_logged_out.html"))
var loggedInMenu = template.Must(pages.HtmlPage.ParseFS(templatesFS, "templates/navbar_logged_in.html"))

func GetLoggedInMenu(username string, url string) (*bytes.Buffer, error) {
	url_parts := strings.Split(url, "/")
	params := LoggedInMenuComponent{
		Username: username,
		Entity:   url_parts[len(url_parts)-1],
		IsAdmin:  username == "Romain", // :hack:
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
