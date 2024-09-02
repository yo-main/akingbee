package templates

import (
	"akingbee/api/templates/icons"
	"bytes"
	// "io"
	// "log"
	// "os"
	"text/template"
)

type htmlPageComponent struct {
	LogoImage string
	LogoText  string
	Head      string
	Body      string
}

const htmlHead = `
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Akingbee</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@1.0.2/css/bulma.min.css">
      </head>
`

const htmlBase = `
	<!DOCTYPE html>
    <html>
    {{ .Head }}
    {{ .Body }}
</html>
`

func BuildPage(body string) ([]byte, error) {

	params := htmlPageComponent{
		Head:      htmlHead,
		LogoImage: icons.AkingbeeLogoImage,
		LogoText:  icons.AkingbeeLogoText,
		Body:      body,
	}

	tmpl, err := template.New("HtmlPage").Parse(htmlBase)

	if err != nil {
		return nil, err
	}

	var buffer bytes.Buffer
	tmpl.Execute(&buffer, params)

	return buffer.Bytes(), nil

}
