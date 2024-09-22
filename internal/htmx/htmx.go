package htmx

import (
	"net/http"
)

func IsHtmxRequest(req *http.Request) bool {
	return req.Header.Get("HX-Request") != ""
}

func Redirect(response http.ResponseWriter, url string) {
	response.Header().Set("HX-Redirect", url)
}

func PushUrl(response http.ResponseWriter, url string) {
	response.Header().Set("HX-Push-Url", url)
}
