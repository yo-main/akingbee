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

		events := map[string]interface{}{
			"notificationEvent": templates.BuildErrorNotification(err.Error()),
		}
		triggerHeader, _ := json.Marshal(events)
		response.Header().Set("HX-Trigger", string(triggerHeader))
		response.WriteHeader(http.StatusBadRequest)

		return
	}

	user, err := user_service.CreateUser(ctx, &command)
	if err != nil {

		events := map[string]interface{}{
			"notificationEvent": templates.BuildErrorNotification(err.Error()),
		}
		triggerHeader, _ := json.Marshal(events)
		response.Header().Set("HX-Trigger", string(triggerHeader))
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	_, err = userToJson(user)
	if err != nil {

		events := map[string]interface{}{
			"notificationEvent": templates.BuildErrorNotification(err.Error()),
		}
		triggerHeader, _ := json.Marshal(events)
		response.Header().Set("HX-Trigger", string(triggerHeader))

		response.WriteHeader(http.StatusBadRequest)
		return
	}

	events := map[string]interface{}{
		"notificationEvent": templates.BuildSuccessNotification("User created successfully"),
	}
	triggerHeader, _ := json.Marshal(events)
	response.Header().Set("HX-Trigger", string(triggerHeader))
	response.WriteHeader(http.StatusOK)
}
