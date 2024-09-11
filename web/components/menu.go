package components

import (
	"akingbee/web/pages"
	"bytes"
	"html/template"
)

type menuComponent struct {
}

var loggedOutMenu = template.Must(pages.HtmlPage.ParseFiles("web/components/templates/navbar_logged_out.html"))
var loggedInMenu = template.Must(pages.HtmlPage.ParseFiles("web/components/templates/navbar_logged_in.html"))

var logoIcon = template.Must(pages.HtmlPage.ParseFiles("web/icons/logo.html"))
var akingbeeIcon = template.Must(pages.HtmlPage.ParseFiles("web/icons/akingbee.html"))

func GetLoggedInMenu() (template.HTML, error) {
	params := menuComponent{}

	var buffer bytes.Buffer
	loggedInMenu.ExecuteTemplate(&buffer, "navbar_logged_in.html", params)

	return template.HTML(buffer.Bytes()), nil

}

func GetLoggedOutMenu() (template.HTML, error) {
	params := menuComponent{}

	var buffer bytes.Buffer
	loggedOutMenu.ExecuteTemplate(&buffer, "navbar_logged_out.html", params)

	return template.HTML(buffer.Bytes()), nil

}
