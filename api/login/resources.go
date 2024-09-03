package login

import (
	"akingbee/api/templates"
	"log"
	"net/http"
)

const loginForm = `
<div class="columns is-centered">

  <div class="column is-narrow">
    <div class="content has-text-centered">
      <p class="subtitle">Bienvenue sur <strong>Akingbee</strong>!</p>
    </div>

    <div class="field pt-5 is-horizontal">
      <div class="field-label is-flex-grow-4">Identifiant</div>
      <div class="field-body">
        <div class="control">
          <input class="input" type="text">
        </div>
      </div>
    </div>
    <div class="field is-horizontal">
      <div class="field-label is-normal is-flex-grow-4">Mot de passe</div>
      <div class="field-body">
        <div class="control">
          <input class="input" type="password">
        </div>
      </div>
    </div>
    <div class="field is-grouped is-grouped-right">
      <div class="control">
        <button class="button">Mot de passe oublié ?</button>
      </div>
      <div class="control">
        <button class="button is-link">Se connecter</button>
      </div>
    </div>
  </div>
</div>
`

func HandleGetLogin(response http.ResponseWriter, req *http.Request) {
	log.Print("GOT A LOGIN REQUEST")

	menu, err := templates.GetLoggedOutMenu()
	if err != nil {
		log.Printf("NOOOO FAILED: %s", err)
		return
	}

	page, err := templates.BuildPage(templates.BuildBody(loginForm, menu))
	if err != nil {
		log.Printf("NOOOO FAILED: %s", err)
		return
	}

	response.Write([]byte(page))
}
