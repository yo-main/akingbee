package api

import (
	_ "akingbee/bees/models"
	apiary_service "akingbee/bees/services/apiary"
	"akingbee/web"
	"net/http"
)

func HandlePostApiary(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()

	command := apiary_service.CreateApiaryCommand{
		Name:      req.FormValue("name"),
		Location:  req.FormValue("location"),
		HoneyKind: req.FormValue("honeyKind"),
	}

	err := command.Validate()
	if err != nil {
		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	user, err := apiary_service.CreateApiary(ctx, &command)
	if err != nil {

		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	_, err = userToJson(user)
	if err != nil {

		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	web.PrepareSuccessNotification(response, "User created successfully")
	response.WriteHeader(http.StatusOK)

}
