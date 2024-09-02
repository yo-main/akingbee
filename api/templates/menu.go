package templates

import (
	"akingbee/api/templates/icons"
	"bytes"
	"text/template"
)

type menuComponent struct {
	LogoImage string
	LogoText  string
}

const loggedInMenu = `
<nav class="navbar is-fixed-top has-background-warning-95 has-shadow">
    <div class="navbar-brand">
		{{ .LogoImage }}
		{{ .LogoText }}
    </div>
    <div class="navbar-menu has-text-inherit">

	<div class="navbar-start has-text-inherit">
		<p class="navbar-item"><a class="has-text-warning-95-invert">Ruches</a></p>
		<p class="navbar-item"><a class="has-text-warning-95-invert">Ruchers</a></p>
		<p class="navbar-item"><a class="has-text-warning-95-invert">Paramètres</a></p>
	</div>

	<div class="navbar-end">
		<p class="navbar-item"><strong class="has-text-warning-95-invert">Bienvenue Romain</strong></p>
		<p class="navbar-item"><a class="has-text-warning-95-invert">Déconnexion</a></p>
	</div>
</nav>
`

func GetLoggedInMenu() (string, error) {
	params := menuComponent{
		LogoImage: icons.AkingbeeLogoImage,
		LogoText:  icons.AkingbeeLogoText,
	}

	tmpl, err := template.New("LoggedInMenu").Parse(loggedInMenu)

	if err != nil {
		return "", err
	}

	var buffer bytes.Buffer
	tmpl.Execute(&buffer, params)

	return buffer.String(), nil

}
