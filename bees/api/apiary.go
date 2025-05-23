package api

import (
	"log"
	"net/http"

	"github.com/google/uuid"

	"akingbee/bees/pages"
	"akingbee/bees/repositories"
	apiary_services "akingbee/bees/services/apiary"
	api_helpers "akingbee/internal/web"
	user_models "akingbee/user/models"
	"akingbee/web"
)

func HandlePostApiary(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()

	if user, ok := ctx.Value("authenticatedUser").(*user_models.AuthenticatedUser); ok {

		command := apiary_services.CreateApiaryCommand{
			Name:      req.FormValue("name"),
			Location:  req.FormValue("location"),
			HoneyKind: req.FormValue("honeyKind"),
			User:      &user.PublicID,
		}

		_, err := apiary_services.CreateApiary(ctx, &command)
		if err != nil {
			log.Printf("Could not create apiary: %s", err)
			web.PrepareFailedNotification(response, err.Error())
			response.WriteHeader(http.StatusBadRequest)
			return
		}

		apiaryPage, err := pages.GetApiaryBody(ctx, &user.PublicID)
		if err != nil {
			log.Printf("Could not get apiary page: %s", err)
			http.Redirect(response, req, "/", http.StatusMovedPermanently)
			return
		}

		web.PrepareSuccessNotification(response, "Apiary created successfully")
		response.WriteHeader(http.StatusOK)
		api_helpers.WriteToResponse(response, apiaryPage.Bytes())
	} else {
		panic("unreacheable")
	}
}

func HandlePutApiary(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()

	user, ok := ctx.Value("authenticatedUser").(*user_models.AuthenticatedUser)
	if ok == false {
		panic("unreacheable")
	}

	apiaryPublicID, err := uuid.Parse(req.PathValue("apiaryPublicId"))
	if err != nil {
		log.Printf("The provided apiary id is incorrect: %s", err)
		web.PrepareFailedNotification(response, "Bad request")
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	apiary, err := repositories.GetApiary(ctx, &apiaryPublicID)
	if err != nil {
		log.Printf("Apiary not found: %s", err)
		web.PrepareFailedNotification(response, "Apiary not found")
		response.WriteHeader(http.StatusNotFound)
		return
	}

	if apiary.User != user.PublicID {
		response.WriteHeader(http.StatusForbidden)
		web.PrepareFailedNotification(response, "Forbidden")
		return
	}

	apiary.Name = req.FormValue("name")
	apiary.Location = req.FormValue("location")
	apiary.HoneyKind = req.FormValue("honeyKind")

	err = apiary_services.UpdateApiary(ctx, apiary)
	if err != nil {
		log.Printf("Could not update apiary: %s", err)
		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	tableRow := pages.GetApiaryTableRow(apiary)
	content, err := tableRow.Build()
	if err != nil {
		log.Printf("Could not get table row: %s", err)
		http.Redirect(response, req, "/", http.StatusBadRequest)
		return
	}

	web.PrepareSuccessNotification(response, "Apiary updated successfully")
	response.WriteHeader(http.StatusOK)
	api_helpers.WriteToResponse(response, content.Bytes())
}

func HandleDeleteApiary(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()
	user, ok := ctx.Value("authenticatedUser").(*user_models.AuthenticatedUser)

	if ok == false {
		panic("unreacheable")
	}

	apiaryPublicID, err := uuid.Parse(req.PathValue("apiaryPublicId"))
	if err != nil {
		log.Printf("The provided apiary id is incorrect: %s", err)
		web.PrepareFailedNotification(response, "Bad request")
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	apiary, err := repositories.GetApiary(ctx, &apiaryPublicID)
	if err != nil {
		log.Printf("Apiary not found: %s", err)
		web.PrepareFailedNotification(response, "Apiary not found")
		response.WriteHeader(http.StatusNotFound)
		return
	}

	if apiary.User != user.PublicID {
		response.WriteHeader(http.StatusForbidden)
		web.PrepareFailedNotification(response, "Forbidden")
		return
	}

	err = apiary_services.DeleteApiary(ctx, apiary)
	if err != nil {
		log.Printf("Could not delete apiary: %s", err)
		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	web.PrepareSuccessNotification(response, "Apiary deleted successfully")
	response.WriteHeader(http.StatusOK)
}
