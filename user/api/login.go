package user

import (
	"fmt"
	"log"
	"net/http"

	"github.com/google/uuid"

	"akingbee/internal/htmx"
	api_helpers "akingbee/internal/web"
	"akingbee/user/models"
	user_pages "akingbee/user/pages"
	"akingbee/user/repositories"
	"akingbee/user/services"
	"akingbee/web"
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

	user, err := repositories.GetUserByUsername(ctx, &username)
	if err != nil {
		log.Printf("Could not get user by username with %s: %s", username, err)
		web.PrepareFailedNotification(response, "Invalid Credentials")
		response.WriteHeader(http.StatusBadRequest)

		return
	}

	token, err := services.LoginUser(password, user)

	if err != nil {
		log.Printf("Login failure: %s", err)
		web.PrepareFailedNotification(response, "Invalid Credentials")
		response.WriteHeader(http.StatusBadRequest)

		return
	}

	welcomePage, err := user_pages.GetWelcomePage(req)
	if err != nil {
		log.Printf("Could not build welcome page: %s", err)
		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)

		return
	}

	htmx.PushURL(response, "/")
	web.PrepareLoggedInMenu(req, response, &models.AuthenticatedUser{User: user, Impersonator: nil})
	web.PrepareSuccessNotification(response, fmt.Sprintf("Hello %s !", username))
	response.Header().Set("Set-Cookie", fmt.Sprintf("%s=%s; Path=/; HttpOnly; Secure", "akingbeeToken", token))
	api_helpers.WriteToResponse(response, welcomePage.Bytes())
}

func HandleLogout(response http.ResponseWriter, req *http.Request) {
	response.Header().Set("Set-Cookie", "akingbeeToken=''; Path=/; expire;")
	web.PrepareLoggedOutMenu(response)
	htmx.PushURL(response, "/")

	welcomePage, err := user_pages.GetWelcomePage(req)
	if err != nil {
		log.Printf("Could not load welcome page: %s", err)
	} else {
		api_helpers.WriteToResponse(response, welcomePage.Bytes())
	}
}

func HandleImpersonate(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()

	impersonatedUser, err := uuid.Parse(req.PathValue("userPublicId"))

	if err != nil {
		response.WriteHeader(http.StatusNotFound)
		return
	}

	loggedUser, err := services.AuthenticateUser(req)
	if err != nil {
		log.Printf("Login failure: %s", err)
		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)

		return
	}

	token, err := services.ImpersonateUser(ctx, &loggedUser.User.PublicID, &impersonatedUser)

	if err != nil {
		log.Printf("Login failure: %s", err)
		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)

		return
	}

	welcomePage, err := user_pages.GetWelcomePage(req)
	if err != nil {
		log.Printf("Could not build welcome page: %s", err)
		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)

		return
	}

	web.PrepareLoggedInMenu(req, response, loggedUser)
	web.PrepareSuccessNotification(response, fmt.Sprintf("Successfully impersonating user %s !", impersonatedUser))
	response.Header().Set("Set-Cookie", fmt.Sprintf("%s=%s; Path=/; HttpOnly; Secure", "akingbeeToken", token))
	api_helpers.WriteToResponse(response, welcomePage.Bytes())
}
