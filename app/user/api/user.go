package user

import (
	"akingbee/app/core/api"
	user_service "akingbee/app/user"
	"akingbee/app/user/models"
	"encoding/json"
	"fmt"
	"net/http"
)

func userToJson(user *models.User) ([]byte, error) {
	data := map[string]interface{}{
		"publicId": user.PublicId,
		"email":    user.Email,
		"username": user.Credentials.Username,
	}

	return json.Marshal(data)
}

func HandlePostUser(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()

	command := user_service.CreateUserCommand{
		Username: req.FormValue("username"),
		Password: req.FormValue("password"),
		Email:    req.FormValue("email"),
	}

	err := command.Validate()
	if err != nil {
		api.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	user, err := user_service.CreateUser(ctx, &command)
	if err != nil {

		api.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	_, err = userToJson(user)
	if err != nil {

		api.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	api.PrepareSuccessNotification(response, "User created successfully")
	response.WriteHeader(http.StatusOK)
}

func HandleLoginUser(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()

	username := req.FormValue("username")
	password := req.FormValue("password")

	_, err := user_service.LoginUser(ctx, username, password)

	if err != nil {
		api.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	api.PrepareSuccessNotification(response, fmt.Sprintf("Hello %s !", username))
	response.WriteHeader(http.StatusOK)
}
