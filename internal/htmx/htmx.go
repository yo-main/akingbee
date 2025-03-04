package htmx

import (
	"net/http"
)

func IsHtmxRequest(req *http.Request) bool {
	return req.Header.Get("Hx-Request") != ""
}

func Redirect(response http.ResponseWriter, url string) {
	response.Header().Set("Hx-Redirect", url)
}

func PushURL(response http.ResponseWriter, url string) {
	response.Header().Set("Hx-Push-Url", url)
}
