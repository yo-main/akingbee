package api

import (
	"akingbee/bees/pages"
	"akingbee/bees/repositories"
	hive_services "akingbee/bees/services/hive"
	user_services "akingbee/user/services"
	"akingbee/web"
	"fmt"
	"log"
	"net/http"

	"github.com/google/uuid"
)

func HandlePostHive(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()

	userId, err := user_services.AuthenticateUser(req)

	if err != nil {
		log.Printf("Could not authenticate user: %s", err)
		web.PrepareFailedNotification(response, "Not authenticated")
		response.WriteHeader(http.StatusUnauthorized)
		return
	}

	var apiaryPublicId *uuid.UUID
	if !(req.FormValue("apiary") == "none" || req.FormValue("apiary") == "") {
		result, err := uuid.Parse(req.FormValue("apiary"))
		if err != nil {
			log.Printf("Wrong apiary id: %s", req.FormValue("apiary"))
			web.PrepareFailedNotification(response, fmt.Sprintf("Invalid apiary id: %s", req.FormValue("apiary")))
			response.WriteHeader(http.StatusBadRequest)
			return
		}
		apiaryPublicId = &result
	}
	command := hive_services.CreateHiveCommand{
		Name:      req.FormValue("name"),
		Condition: req.FormValue("condition"),
		Apiary:    apiaryPublicId,
		Owner:     userId,
	}

	_, err = hive_services.CreateHive(ctx, &command)
	if err != nil {
		log.Printf("Could not create hive: %s", err)
		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	hivePage, err := pages.GetHivesBody(ctx, userId)
	if err != nil {
		log.Printf("Could not get hives page: %s", err)
		http.Redirect(response, req, "/", http.StatusMovedPermanently)
		return
	}

	web.PrepareSuccessNotification(response, "Hive created successfully")
	response.WriteHeader(http.StatusOK)
	response.Write(hivePage.Bytes())
}

func HandlePutHive(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()

	userId, err := user_services.AuthenticateUser(req)

	if err != nil {
		log.Printf("Could not authenticate user: %s", err)
		web.PrepareFailedNotification(response, "Not authenticated")
		response.WriteHeader(http.StatusUnauthorized)
		return
	}

	hivePublicId, err := uuid.Parse(req.PathValue("hivePublicId"))
	if err != nil {
		log.Printf("The provided hive id is incorrect: %s", err)
		web.PrepareFailedNotification(response, "Bad request")
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	hive, err := repositories.GetHive(ctx, &hivePublicId)
	if err != nil {
		log.Printf("Hive not found: %s", err)
		web.PrepareFailedNotification(response, "Hive not found")
		response.WriteHeader(http.StatusNotFound)
		return
	}

	if hive.Owner != *userId {
		response.WriteHeader(http.StatusForbidden)
		web.PrepareFailedNotification(response, "Forbidden")
		return
	}

	hive.Name = req.FormValue("name")
	hive.Condition = req.FormValue("condition")

	err = hive_services.UpdateHive(ctx, hive)
	if err != nil {
		log.Printf("Could not update hive: %s", err)
		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	tableRow := pages.GetHiveTableRow(hive)
	content, err := tableRow.Build()
	if err != nil {
		log.Printf("Could not get table row: %s", err)
		http.Redirect(response, req, "/", http.StatusBadRequest)
		return
	}

	web.PrepareSuccessNotification(response, "Hive updated successfully")
	response.WriteHeader(http.StatusOK)
	response.Write(content.Bytes())
}

func HandleDeleteHive(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()

	userId, err := user_services.AuthenticateUser(req)

	if err != nil {
		log.Printf("Could not authenticate user: %s", err)
		web.PrepareFailedNotification(response, "Not authenticated")
		response.WriteHeader(http.StatusUnauthorized)
		return
	}

	hivePublicId, err := uuid.Parse(req.PathValue("hivePublicId"))
	if err != nil {
		log.Printf("The provided hive id is incorrect: %s", err)
		web.PrepareFailedNotification(response, "Bad request")
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	hive, err := repositories.GetHive(ctx, &hivePublicId)
	if err != nil {
		log.Printf("Hive not found: %s", err)
		web.PrepareFailedNotification(response, "Hive not found")
		response.WriteHeader(http.StatusNotFound)
		return
	}

	if hive.Owner != *userId {
		response.WriteHeader(http.StatusForbidden)
		web.PrepareFailedNotification(response, "Forbidden")
		return
	}

	err = hive_services.DeleteHive(ctx, hive)
	if err != nil {
		log.Printf("Could not delete hive: %s", err)
		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	web.PrepareSuccessNotification(response, "Hive deleted successfully")
	response.WriteHeader(http.StatusOK)
}
