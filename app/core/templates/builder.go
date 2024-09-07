package templates

import (
	"bytes"
	"fmt"
	"text/template"
)

type htmlPageComponent struct {
	Head string
	Body string
}

const htmlHead = `
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

		<meta name="htmx-config" content='{"selfRequestsOnly":false}'>

        <title>Akingbee</title>

		<script src="https://unpkg.com/htmx.org@2.0.2" integrity="sha384-Y7hw+L/jvKeWIRRkqWYfPcvVxHzVzn5REgzbawhxAuQGwX1XWe70vji+VSeHOThJ" crossorigin="anonymous"></script>

        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@1.0.2/css/bulma.min.css">
		<link rel="stylesheet" href="custom.css" />
      </head>
`

const htmlBase = `
	<!DOCTYPE html>
    <html>
    {{ .Head }}
    {{ .Body }}
		<script src="custom.js"></script>
</html>
`

func BuildPage(body string) ([]byte, error) {

	params := htmlPageComponent{
		Head: htmlHead,
		Body: body,
	}

	tmpl, err := template.New("HtmlPage").Parse(htmlBase)

	if err != nil {
		return nil, err
	}

	var buffer bytes.Buffer
	tmpl.Execute(&buffer, params)

	return buffer.Bytes(), nil

}

func BuildBody(content string, menu string) string {
	return fmt.Sprintf(`
	  <body class="has-navbar-fixed-top">
		<section class="section">
			%s
		</section>

		<div id="notificationBox" hx-trigger="notificationEvent from:body" hx-get="data:text/html," hx-on:htmx:after-swap="htmx.swap(this, event.detail.requestConfig.triggeringEvent.detail.value, {swapStyle: 'afterbegin'})"></div>

		<section class="hero is-fullheight-with-navbar has-background-white-lighter">
			%s
		</section>

	    <div class="container p-5">
	      <div class="content has-text-centered">
	        <p>Made with love by Yomain</p>
	      </div>
	    </div>
	  </body>
	`, menu, content)
}

func BuildSuccessNotification(content string) string {
	return fmt.Sprintf(`
	<div class="notification is-success">
		<button class="delete" hx-get="data:text/html," hx-target="closest .notification" hx-swap="delete"></button>
		<div>%s</div>
	</div>
	`, content)
}

func BuildErrorNotification(content string) string {
	return fmt.Sprintf(`
	<div class="notification is-danger">
		<button class="delete" hx-get="data:text/html," hx-target="closest .notification" hx-swap="delete"></button>
		<div>%s</div>
	</div>
	`, content)
}
