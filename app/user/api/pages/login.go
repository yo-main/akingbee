package login

import (
	"akingbee/app/core/api/templates"
	"bytes"
	"html/template"
	"net/http"
)

var loginPageTemplate = template.Must(template.New("loginPage").Parse(`
<div class="columns is-centered">
  <div class="column is-narrow">

    <div class="content has-text-centered">
      <p class="subtitle">Bienvenue sur <strong>Akingbee</strong>!</p>
    </div>

	{{ .Form }}

  </div>
</div>
`))

type loginPageParams struct {
	Form template.HTML
}

func HandleGetLogin(response http.ResponseWriter, req *http.Request) {
	menu, err := templates.GetLoggedOutMenu()
	if err != nil {
		return
	}

	form := templates.Form{
		Id:     "login",
		Method: "post",
		Target: "/login",
		SubmitButton: templates.Button{
			Label: "Se connecter",
			Swap:  "none",
		},
		Inputs: []templates.Input{
			{
				Name:     "login",
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
	}

	formStr, err := form.Build()
	var loginPage bytes.Buffer

	err = loginPageTemplate.Execute(&loginPage, loginPageParams{Form: formStr})
	page, err := templates.BuildPage(templates.BuildBody(template.HTML(loginPage.Bytes()), menu))

	if err != nil {
		return
	}

	response.Write([]byte(page))
}

func HandleWelcomePage(response http.ResponseWriter, req *http.Request) {
	http.Redirect(response, req, "/login", http.StatusMovedPermanently)
}
