package user

import (
	"akingbee/app/core/templates"
	user_service "akingbee/app/user"
	"akingbee/app/user/models"
	"encoding/json"
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
		response.WriteHeader(http.StatusBadRequest)
		response.Write([]byte(err.Error()))
		return
	}

	user, err := user_service.CreateUser(ctx, &command)
	if err != nil {
		response.WriteHeader(http.StatusBadRequest)
		response.Write([]byte(err.Error()))
		return
	}

	_, err = userToJson(user)
	if err != nil {
		response.WriteHeader(http.StatusBadRequest)
		response.Write([]byte(err.Error()))
		return
	}

	response.WriteHeader(http.StatusOK)
	response.Write([]byte(templates.BuildSuccessNotification("User created successfully")))
}