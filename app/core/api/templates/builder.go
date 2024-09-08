package templates

import (
	"bytes"
	"fmt"
	"html/template"
	"log"
)

type htmlPageComponent struct {
	Body template.HTML
}

var htmlBase = template.Must(template.New("htmlBase").Parse(`
	<!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

		<meta name="htmx-config" content='{"selfRequestsOnly":false}'>

        <title>Akingbee</title>

		<script src="https://unpkg.com/htmx.org@2.0.2" integrity="sha384-Y7hw+L/jvKeWIRRkqWYfPcvVxHzVzn5REgzbawhxAuQGwX1XWe70vji+VSeHOThJ" crossorigin="anonymous"></script>

        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@1.0.2/css/bulma.min.css">
		<link rel="stylesheet" href="custom.css" />
    </head>
    {{ .Body }}
</html>
`))

func BuildPage(body template.HTML) ([]byte, error) {

	params := htmlPageComponent{
		Body: body,
	}

	var buffer bytes.Buffer
	err := htmlBase.Execute(&buffer, params)
	if err != nil {
		log.Printf("Error while building html page: %s", err)
	}

	return buffer.Bytes(), nil

}

func BuildBody(content template.HTML, menu template.HTML) template.HTML {
	return template.HTML(fmt.Sprintf(`
	  <body class="has-navbar-fixed-top">
		<section class="section">
			%s
		</section>

		<div id="notificationBox" hx-trigger="notificationEvent from:body" hx-get="data:text/html," hx-swap="none" hx-on:htmx:after-settle="if (event.detail.requestConfig != null) {htmx.swap(this, event.detail.requestConfig.triggeringEvent.detail.value, {swapStyle: 'afterbegin'})}"></div>

		<section class="hero is-fullheight-with-navbar has-background-white-lighter">
			%s
		</section>

	    <div class="container p-5">
	      <div class="content has-text-centered">
	        <p>Made with love by Yomain</p>
	      </div>
	    </div>
	  </body>
	`, menu, content))
}

func BuildSuccessNotification(content string) template.HTML {
	return template.HTML(fmt.Sprintf(`
	<div class="notification is-success">
		<button class="delete" hx-get="data:text/html," hx-target="closest .notification" hx-swap="delete"></button>
		<div>%s</div>
	</div>
	`, content))
}

func BuildErrorNotification(content string) template.HTML {
	return template.HTML(fmt.Sprintf(`
	<div class="notification is-danger">
		<button class="delete" hx-get="data:text/html," hx-target="closest .notification" hx-swap="delete"></button>
		<div>%s</div>
	</div>
	`, content))
}
