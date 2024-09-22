package components

import (
	"akingbee/web/pages"
	"bytes"
	"html/template"
)

type LoggedInMenuComponent struct {
	Username string
}

type LoggedOutMenuComponent struct {
}

var loggedOutMenu = template.Must(pages.HtmlPage.ParseFiles("web/components/templates/navbar_logged_out.html"))
var loggedInMenu = template.Must(pages.HtmlPage.ParseFiles("web/components/templates/navbar_logged_in.html"))

func GetLoggedInMenu(username string) (*bytes.Buffer, error) {
	params := LoggedInMenuComponent{
		Username: username,
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
