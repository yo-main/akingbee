package entrypoints

import (
	api_apiary "akingbee/bees/api"
	pages_bees "akingbee/bees/pages"
	api_user "akingbee/user/api"
	pages_user "akingbee/user/pages"
	"log"
	"net/http"
)

func ApiServe() {
	fs := http.FileServer(http.Dir("web/resources/"))

	mux := http.NewServeMux()

	mux.Handle("/", fs)
	mux.HandleFunc("GET /{$}", pages_user.HandleWelcomePage)

	mux.HandleFunc("POST /logout", api_user.HandleLogout)

	mux.HandleFunc("GET /login", pages_user.HandleGetLogin)
	mux.HandleFunc("POST /login", api_user.HandlePostLogin)

	mux.HandleFunc("GET /register", pages_user.HandleGetRegister)
	mux.HandleFunc("POST /users", api_user.HandlePostUser)

	mux.HandleFunc("GET /apiary", pages_bees.HandleGetApiary)
	mux.HandleFunc("POST /apiary", api_apiary.HandlePostApiary)

	// http.HandleFunc("POST /login", login.UserLogin)

	// http.HandleFunc("GET /user/{id}", user.GetUser)
	// http.HandleFunc("GET /users", user.GetUsers)
	// http.Handle("/", fs)

	log.Print("Listing on port 8080...\n")
	http.ListenAndServe(":8080", mux)
}
