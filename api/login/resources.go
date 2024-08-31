package login

import (
	"log"
	"net/http"
)

func HandleGetLogin(response http.ResponseWriter, req *http.Request) {
	log.Print("GOT A LOGIN REQUEST")
	response.Write([]byte(`
		<!DOCTYPE html>
			<html>
				<body>COUCOUCOUCOCU
		</body></html>
	`))
}
