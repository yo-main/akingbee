package api

import (
	"akingbee/bees/pages"
	apiary_services "akingbee/bees/services/apiary"
	user_services "akingbee/user/services"
	"akingbee/web"
	"log"
	"net/http"
)

func HandlePostApiary(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()

	userId, err := user_services.AuthenticateUser(req)

	if err != nil {
		log.Printf("Could not authenticate user: %s", err)
		response.WriteHeader(http.StatusUnauthorized)
		return
	}

	command := apiary_services.CreateApiaryCommand{
		Name:      req.FormValue("name"),
		Location:  req.FormValue("location"),
		HoneyKind: req.FormValue("honeyKind"),
		Owner:     userId,
	}

	_, err = apiary_services.CreateApiary(ctx, &command)
	if err != nil {
		log.Printf("Could not create apiary: %s", err)
		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	apiaryPage, err := pages.GetApiaryBody(ctx, userId)
	if err != nil {
		log.Printf("Could not get apiary page: %s", err)
		http.Redirect(response, req, "/", http.StatusMovedPermanently)
		return
	}

	web.PrepareSuccessNotification(response, "Apiary created successfully")
	response.WriteHeader(http.StatusOK)
	response.Write(apiaryPage.Bytes())
}
