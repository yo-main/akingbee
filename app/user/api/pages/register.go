package login

import (
	"akingbee/app/core/api/templates"
	"bytes"
	"html/template"

	"log"

	"net/http"
)

var registerPageTemplate = template.Must(template.New("registerPage").Parse(`
<div class="columns is-centered">

  <div class="columns">
	<div class="column">
	  <div class="content has-text-centered">
	    <p class="subtitle">Dites moi en plus sur vous</p>
	  </div>
	  {{ .Form }}
  	</div>
  </div>
</div>
`))

type registerPageParams struct {
	Form template.HTML
}

func HandleGetRegister(response http.ResponseWriter, req *http.Request) {
	menu, err := templates.GetLoggedOutMenu()
	if err != nil {
		return
	}

	form := templates.Form{
		Id:     "post-user",
		Method: "post",
		Target: "/users",
		SubmitButton: templates.Button{
			Label: "S'enregistrer",
			Swap:  "none",
		},
		Inputs: []templates.Input{
			{
				Name:     "email",
				Label:    "Email",
				Type:     "email",
				Required: true,
			},
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
	}

	formStr, err := form.Build()
	var registerPage bytes.Buffer
	err = registerPageTemplate.Execute(&registerPage, registerPageParams{Form: formStr})

	log.Printf("%s - %s", formStr, err)

	page, err := templates.BuildPage(templates.BuildBody(template.HTML(registerPage.Bytes()), menu))
	if err != nil {
		return
	}

	response.Write([]byte(page))
}
