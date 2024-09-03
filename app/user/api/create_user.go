package user

import (
	"akingbee/api/templates"
	"akingbee/models"
	"log"
	"net/http"
)

func HandlePostUser(response http.ResponseWriter, req *http.Request) {
	username := req.PostForm.Get("username")
	password := req.PostForm.Get("password")


	user := models.User{
		PublicId: ,
	}

	
}
