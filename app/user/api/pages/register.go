package login

import (
	"akingbee/app/core/templates"
	"net/http"
)

const registerForm = `
<div class="columns is-centered">

  <form>
    <div class="column is-narrow">
      <div class="content has-text-centered">
        <p class="subtitle">Dites moi en plus sur vous</p>
      </div>

      <div class="field pt-5 is-horizontal">
        <div class="field-label is-normal is-flex-grow-4">Votre email</div>
        <div class="field-body">
          <div class="control">
            <input class="input" type="text" name="email">
          </div>
        </div>
      </div>

      <div class="field is-horizontal">
        <div class="field-label is-normal is-flex-grow-4">Votre identifiant</div>
        <div class="field-body">
          <div class="control">
            <input class="input" type="text" name="username">
          </div>
        </div>
      </div>

      <div class="field is-horizontal">
        <div class="field-label is-normal is-flex-grow-4">Votre mot de passe</div>
        <div class="field-body">
          <div class="control">
            <input class="input" type="password" name="password">
          </div>
        </div>
      </div>
      <div class="field is-grouped is-grouped-right">
        <div class="control">
          <button class="button is-link" hx-post="/users" hx-swap="none">
              S'enregister
          </button>
        </div>
      </div>
    </div>
  </form>
</div>
`

func HandleGetRegister(response http.ResponseWriter, req *http.Request) {
	menu, err := templates.GetLoggedOutMenu()
	if err != nil {
		return
	}

	page, err := templates.BuildPage(templates.BuildBody(registerForm, menu))
	if err != nil {
		return
	}

	response.Write([]byte(page))
}
