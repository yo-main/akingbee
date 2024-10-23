package entrypoints

import (
	api_bees "akingbee/bees/api"
	pages_bees "akingbee/bees/pages"
	api_user "akingbee/user/api"
	pages_user "akingbee/user/pages"
	user_services "akingbee/user/services"
	"log"
	"net/http"

	"github.com/google/uuid"
)

func Authenticated(callback func(response http.ResponseWriter, req *http.Request, userId *uuid.UUID)) func(response http.ResponseWriter, req *http.Request) {

	return func(response http.ResponseWriter, req *http.Request) {
		userId, err := user_services.AuthenticateUser(req)

		if err != nil {
			log.Printf("Could not authenticate user: %s", err)
			response.WriteHeader(http.StatusUnauthorized)
			return
		}

		callback(response, req, userId)
	}
}

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

	mux.HandleFunc("GET /apiary", Authenticated(pages_bees.HandleGetApiary))
	mux.HandleFunc("POST /apiary", Authenticated(api_bees.HandlePostApiary))
	mux.HandleFunc("PUT /apiary/{apiaryPublicId}", Authenticated(api_bees.HandlePutApiary))
	mux.HandleFunc("DELETE /apiary/{apiaryPublicId}", Authenticated(api_bees.HandleDeleteApiary))

	mux.HandleFunc("GET /hive", Authenticated(pages_bees.HandleGetHive))
	mux.HandleFunc("POST /hive", Authenticated(api_bees.HandlePostHive))
	mux.HandleFunc("GET /hive/{hivePublicId}", Authenticated(pages_bees.HandleGetHiveDetail))
	mux.HandleFunc("PUT /hive/{hivePublicId}", Authenticated(api_bees.HandlePutHive))
	mux.HandleFunc("DELETE /hive/{hivePublicId}", Authenticated(api_bees.HandleDeleteHive))

	mux.HandleFunc("GET /hive/{hivePublicId}/comments", Authenticated(pages_bees.HandleGetHiveComments))
	mux.HandleFunc("GET /hive/{hivePublicId}/harvests", Authenticated(api_bees.HandleGetHiveHarvests))
	mux.HandleFunc("POST /hive/{hivePublicId}/harvests", Authenticated(api_bees.HandlePostHarvest))
	mux.HandleFunc("DELETE /hive/{hivePublicId}/harvests/{harvestPublicId}", Authenticated(api_bees.HandleDeleteHarvest))

	mux.HandleFunc("POST /comment", Authenticated(api_bees.HandlePostComment))
	mux.HandleFunc("PUT /comment/{commentPublicId}", Authenticated(api_bees.HandlePutComment))
	mux.HandleFunc("DELETE /comment/{commentPublicId}", Authenticated(api_bees.HandleDeleteComment))

	// http.HandleFunc("POST /login", login.UserLogin)

	// http.HandleFunc("GET /user/{id}", user.GetUser)
	// http.HandleFunc("GET /users", user.GetUsers)
	// http.Handle("/", fs)

	log.Print("Listing on port 8080...\n")
	err := http.ListenAndServe(":8080", mux)
	if err != nil {
		log.Printf("Server failed: %s", err)
	}
}
