package user

import (
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

	username := req.PostForm.Get("username")
	password := req.PostForm.Get("password")
	email := req.PostForm.Get("email")

	user, err := user_service.CreateUser(ctx, email, username, password)
	if err != nil {
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	payload, err := userToJson(user)
	if err != nil {
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	response.WriteHeader(http.StatusOK)
	response.Header().Set("Content-Type", "application/json")
	response.Write(payload)
}
