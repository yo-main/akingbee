package entrypoints

import (
	user_api "akingbee/app/user/api"
	user_pages "akingbee/app/user/api/pages"
	"log"
	"net/http"
)

func ApiServe() {
	fs := http.FileServer(http.Dir("front/pages/"))

	mux := http.NewServeMux()

	mux.Handle("/", fs)
	mux.HandleFunc("GET /login", user_pages.HandleGetLogin)

	// http.HandleFunc("POST /login", login.UserLogin)

	// http.HandleFunc("GET /user/{id}", user.GetUser)
	// http.HandleFunc("GET /users", user.GetUsers)
	http.HandleFunc("POST /users", user_api.HandlePostUser)
	// http.Handle("/", fs)

	log.Print("Listing on port 8080...\n")
	http.ListenAndServe(":8080", mux)
}
