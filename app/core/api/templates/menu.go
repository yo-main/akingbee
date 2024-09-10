package templates

import (
	"akingbee/app/core/api/templates/icons"
	"bytes"
	"html/template"
)

type menuComponent struct {
	LogoImage template.HTML
	LogoText  template.HTML
}

var loggedOutMenu = template.Must(HtmlPage.ParseFiles("front/components/navbar_logged_out.html"))
var loggedInMenu = template.Must(HtmlPage.ParseFiles("front/components/navbar_logged_in.html"))

func GetLoggedInMenu() (template.HTML, error) {
	params := menuComponent{
		LogoImage: icons.AkingbeeLogoImage,
		LogoText:  icons.AkingbeeLogoText,
	}

	var buffer bytes.Buffer
	loggedInMenu.ExecuteTemplate(&buffer, "navbar_logged_in.html", params)

	return template.HTML(buffer.Bytes()), nil

}

func GetLoggedOutMenu() (template.HTML, error) {
	params := menuComponent{
		LogoImage: icons.AkingbeeLogoImage,
		LogoText:  icons.AkingbeeLogoText,
	}

	var buffer bytes.Buffer
	loggedOutMenu.ExecuteTemplate(&buffer, "navbar_logged_out.html", params)

	return template.HTML(buffer.Bytes()), nil

}
