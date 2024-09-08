package templates

import (
	"bytes"
	"html/template"
)

var formTemplate = template.Must(template.New("form").Parse(`
	<form
		id="{{ .Id }}"
		hx-{{ .Method }}="{{ .Target }}"
		hx-on:htmx:after-request="if (event.detail.successful) {this.reset()}"
		hx-on:htmx:validation:validate="this.reportValidity()"
	>
      <div class="column is-narrow">

		{{ range .Inputs }}
		  <div class="field is-horizontal">
		    <div class="field-label is-normal is-flex-grow-4">{{ .Label }}</div>
		    <div class="field-body">
		      <div class="control">
				{{ template "input" . }}
		      </div>
		    </div>
		  </div>
		{{ end }}
		
        <div class="field is-grouped is-grouped-right">
          <div class="control">
			{{ template "button" .SubmitButton }}
          </div>
        </div>

      </div>
    </form>
`))

var buttonTemplate = template.Must(formTemplate.New("button").Parse(`
    <button class="button is-link" hx-swap="{{ .Swap }}">
        {{ .Label }}
    </button>
`))

var inputTemplate = template.Must(formTemplate.New("input").Parse(`
<input 
	class="input" 
	type="{{ .Type }}" 
	name="{{ .Name }}" 
	onkeyup="this.setCustomValidity('')" 
	{{ if .Required }}
		hx-on:htmx:validation:validate="if (this.value.length < 1) {this.setCustomValidity('Required')}"
	{{ end}}
>
`))

type Form struct {
	Id           string
	Method       string
	Target       string
	SubmitButton Button
	Inputs       []Input
}

type Button struct {
	Label string
	Swap  string
}

type Input struct {
	Name     string
	Label    string
	Type     string
	Required bool
}

func (form *Form) Build() (template.HTML, error) {
	var buffer bytes.Buffer
	err := formTemplate.Execute(&buffer, form)
	return template.HTML(buffer.Bytes()), err
}
