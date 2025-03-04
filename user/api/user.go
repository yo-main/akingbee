package user

import (
	"log"
	"net/http"

	"akingbee/internal/htmx"
	user_pages "akingbee/user/pages"
	"akingbee/user/services"
	"akingbee/web"
)

func HandlePostUser(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()

	password, err := services.HashPassword(req.FormValue("password"))
	if err != nil {
		log.Printf("Could not hash password: %s", err)
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	command := services.CreateUserCommand{
		Username: req.FormValue("username"),
		Password: password,
		Email:    req.FormValue("email"),
	}

	err = command.Validate()
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

	loginPage, err := user_pages.GetLoginPage()
	if err != nil {
		log.Printf("Could not get welcome page: %s", err)
		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	web.PrepareSuccessNotification(response, "User created successfully")
	htmx.PushURL(response, "/login")
	response.Write(loginPage.Bytes())
	response.WriteHeader(http.StatusOK)
}
