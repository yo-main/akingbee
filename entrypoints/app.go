package entrypoints

import (
	user_api "akingbee/user/api"
	user_pages "akingbee/user/pages"
	"log"
	"net/http"
)

func ApiServe() {
	fs := http.FileServer(http.Dir("web/resources/"))

	mux := http.NewServeMux()

	mux.Handle("/", fs)
	mux.HandleFunc("GET /{$}", user_pages.HandleWelcomePage)
	mux.HandleFunc("GET /login", user_pages.HandleGetLogin)
	mux.HandleFunc("GET /register", user_pages.HandleGetRegister)

	// http.HandleFunc("POST /login", login.UserLogin)

	// http.HandleFunc("GET /user/{id}", user.GetUser)
	// http.HandleFunc("GET /users", user.GetUsers)
	mux.HandleFunc("POST /login", user_api.HandlePostLogin)
	mux.HandleFunc("POST /users", user_api.HandlePostUser)
	// http.Handle("/", fs)

	log.Print("Listing on port 8080...\n")
	http.ListenAndServe(":8080", mux)
}
