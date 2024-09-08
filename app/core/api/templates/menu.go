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

var loggedOutMenu = template.Must(template.New("loggedOutMenu").Parse(`
<nav class="navbar is-fixed-top has-background-warning-95 has-shadow">
    <div class="navbar-brand">
		{{ .LogoImage }}
		{{ .LogoText }}
    </div>
    <div class="navbar-menu has-text-inherit">

	<div class="navbar-end pr-5">
		<p class="navbar-item"><a class="has-text-warning-95-invert">Connexion</a></p>
		<p class="navbar-item"><a class="has-text-warning-95-invert">Inscription</a></p>
	</div>
</nav>
`))

var loggedInMenu = template.Must(template.New("loggedInMenu").Parse(`
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

	<div class="navbar-end pr-5">
		<p class="navbar-item"><strong class="has-text-warning-95-invert">Bienvenue Romain</strong></p>
		<p class="navbar-item"><a class="has-text-warning-95-invert">Déconnexion</a></p>
	</div>
</nav>
`))

func GetLoggedInMenu() (template.HTML, error) {
	params := menuComponent{
		LogoImage: icons.AkingbeeLogoImage,
		LogoText:  icons.AkingbeeLogoText,
	}

	var buffer bytes.Buffer
	loggedInMenu.Execute(&buffer, params)

	return template.HTML(buffer.Bytes()), nil

}

func GetLoggedOutMenu() (template.HTML, error) {
	params := menuComponent{
		LogoImage: icons.AkingbeeLogoImage,
		LogoText:  icons.AkingbeeLogoText,
	}

	var buffer bytes.Buffer
	loggedOutMenu.Execute(&buffer, params)

	return template.HTML(buffer.Bytes()), nil

}
