package login

import (
	"akingbee/api/templates"
	"log"
	"net/http"
)

func HandleGetLogin(response http.ResponseWriter, req *http.Request) {
	log.Print("GOT A LOGIN REQUEST")
	page, err := templates.BuildPage("COUCOUC LOL")
	if err != nil {
		log.Printf("NOOOO FAILED: %s", err)
		return
	}

	response.Write([]byte(page))
}
