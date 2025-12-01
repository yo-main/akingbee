package entrypoints

import (
	"log"
	"net/http"

	api_bees "akingbee/bees/api"
	pages_bees "akingbee/bees/pages"
	"akingbee/internal/web"
	api_journal "akingbee/journal/api"
	api_user "akingbee/user/api"
	pages_user "akingbee/user/pages"
)

func ApiServe() {
	fs := http.FileServer(http.Dir("web/resources/"))

	mux := http.NewServeMux()

	mux.Handle("/public/", fs)
	mux.HandleFunc("GET /{$}", web.OptionallyAuthenticated(web.HtmxMiddleware(pages_user.HandleWelcomePage)))

	mux.HandleFunc("POST /logout", web.OptionallyAuthenticated(api_user.HandleLogout))

	mux.HandleFunc("GET /login", web.OptionallyAuthenticated(web.HtmxMiddleware(pages_user.HandleGetLogin)))
	mux.HandleFunc("POST /login", web.OptionallyAuthenticated(api_user.HandlePostLogin))

	mux.HandleFunc("GET /register", web.OptionallyAuthenticated(web.HtmxMiddleware(pages_user.HandleGetRegister)))
	mux.HandleFunc("POST /users", web.OptionallyAuthenticated(api_user.HandlePostUser))

	mux.HandleFunc("GET /admin", web.Authenticated(web.HtmxMiddleware(pages_user.HandleGetAdmin)))
	mux.HandleFunc("POST /user/{userPublicId}/impersonate", web.Authenticated(web.HtmxMiddleware(api_user.HandleImpersonate)))

	mux.HandleFunc("GET /apiary", web.Authenticated(web.HtmxMiddleware(pages_bees.HandleGetApiary)))
	mux.HandleFunc("POST /apiary", web.Authenticated(api_bees.HandlePostApiary))
	mux.HandleFunc("PUT /apiary/{apiaryPublicId}", web.Authenticated(api_bees.HandlePutApiary))
	mux.HandleFunc("DELETE /apiary/{apiaryPublicId}", web.Authenticated(api_bees.HandleDeleteApiary))

	mux.HandleFunc("GET /hive", web.Authenticated(web.HtmxMiddleware(pages_bees.HandleGetHive)))
	mux.HandleFunc("POST /hive", web.Authenticated(api_bees.HandlePostHive))
	mux.HandleFunc("GET /hive/{hivePublicId}", web.Authenticated(web.HtmxMiddleware(pages_bees.HandleGetHiveDetail)))
	mux.HandleFunc("PUT /hive/{hivePublicId}", web.Authenticated(api_bees.HandlePutHive))
	mux.HandleFunc("DELETE /hive/{hivePublicId}", web.Authenticated(api_bees.HandleDeleteHive))

	mux.HandleFunc("GET /hive/{hivePublicId}/comments", web.Authenticated(web.HtmxMiddleware(pages_bees.HandleGetHiveComments)))
	mux.HandleFunc("POST /hive/{hivePublicId}/comments", web.Authenticated(api_journal.HandlePostCommentHive))
	mux.HandleFunc("PUT /hive/{hivePublicId}/comment/{commentPublicId}", web.Authenticated(api_journal.HandlePutCommentHive))
	mux.HandleFunc("GET /hive/{hivePublicId}/harvests", web.Authenticated(api_bees.HandleGetHiveHarvests))
	mux.HandleFunc("POST /hive/{hivePublicId}/harvests", web.Authenticated(web.HtmxMiddleware(api_bees.HandlePostHarvest)))
	mux.HandleFunc("DELETE /hive/{hivePublicId}/harvests/{harvestPublicId}", web.Authenticated(web.HtmxMiddleware(api_bees.HandleDeleteHarvest)))

	mux.HandleFunc("GET /overview", web.Authenticated(web.HtmxMiddleware(api_journal.HandleGetOverview)))

	mux.HandleFunc("DELETE /comment/{commentPublicId}", web.Authenticated(api_journal.HandleDeleteComment))

	mux.HandleFunc("/", web.OptionallyAuthenticated(web.HtmxMiddleware(web.HandleNotFound)))

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
