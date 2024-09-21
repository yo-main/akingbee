package user

import (
	"akingbee/internal/htmx"
	"akingbee/user/services"
	"akingbee/web"
	"fmt"
	"log"
	"net/http"
)

func HandlePostUser(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()

	command := services.CreateUserCommand{
		Username: req.FormValue("username"),
		Password: req.FormValue("password"),
		Email:    req.FormValue("email"),
	}

	err := command.Validate()
	if err != nil {
		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	_, err = services.CreateUser(ctx, &command)
	if err != nil {

		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	web.PrepareSuccessNotification(response, "User created successfully")
	response.WriteHeader(http.StatusOK)
}

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

	web.PrepareSuccessNotification(response, fmt.Sprintf("Hello %s !", username))
	response.Header().Set("Set-Cookie", fmt.Sprintf("%s=%s; HttpOnly; Secure", "akingbeeToken", token))
	response.WriteHeader(http.StatusOK)
}

func HandleLogout(response http.ResponseWriter, req *http.Request) {
	response.Header().Set("Set-Cookie", "akingbeeToken=''; expire;")
	htmx.Redirect(response, "/")
}
