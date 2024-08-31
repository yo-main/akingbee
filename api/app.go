package api

import (
	// "fmt"
	"akingbee/api/login"
	"log"
	"net/http"
)

func Serve() {
	fs := http.FileServer(http.Dir("front/pages/"))

	mux := http.NewServeMux()

	mux.Handle("/", fs)
	mux.HandleFunc("GET /login", login.HandleGetLogin)

	// http.HandleFunc("POST /login", login.UserLogin)

	// http.HandleFunc("GET /user/{id}", user.GetUser)
	// http.HandleFunc("GET /users", user.GetUsers)
	// http.HandleFunc("POST /users", user.PostUser)
	// http.Handle("/", fs)

	log.Print("Listing on port 8080...\n")
	http.ListenAndServe(":8080", mux)
}
