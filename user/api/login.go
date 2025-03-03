package user

import (
	"akingbee/internal/htmx"
	user_pages "akingbee/user/pages"
	"akingbee/user/services"
	"akingbee/web"
	"fmt"
	"log"
	"net/http"
)

func HandlePostLogin(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()

	username := req.FormValue("username")
	password := req.FormValue("password")

	if len(username) == 0 || len(password) == 0 {
		log.Print("No parameter provided")
		response.WriteHeader(http.StatusBadGateway)
		return
	}

	token, err := services.LoginUser(ctx, username, password)

	if err != nil {
		log.Printf("Login failure: %s", err)
		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	welcomePage, err := user_pages.GetWelcomePage(req)

	htmx.PushUrl(response, "/")
	web.PrepareLoggedInMenu(req, response, username)
	web.PrepareSuccessNotification(response, fmt.Sprintf("Hello %s !", username))
	response.Header().Set("Set-Cookie", fmt.Sprintf("%s=%s; HttpOnly; Secure", "akingbeeToken", token))
	response.Write(welcomePage.Bytes())
}

func HandleLogout(response http.ResponseWriter, req *http.Request) {
	response.Header().Set("Set-Cookie", "akingbeeToken=''; expire;")
	web.PrepareLoggedOutMenu(response)
	htmx.PushUrl(response, "/")

	welcomePage, err := user_pages.GetWelcomePage(req)
	if err != nil {
		log.Printf("Could not load welcome page: %s", err)
	} else {
		response.Write(welcomePage.Bytes())
	}
}
