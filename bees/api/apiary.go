package api

import (
	"akingbee/bees/models"
	_ "akingbee/bees/models"
	apiary_services "akingbee/bees/services/apiary"
	user_services "akingbee/user/services"
	"akingbee/web"
	"encoding/json"
	"log"
	"net/http"
)

func apiaryToJson(apiary *models.Apiary) ([]byte, error) {
	data := map[string]interface{}{
		"publicId":  apiary.PublicId,
		"name":      apiary.Name,
		"location":  apiary.Location,
		"honeyKind": apiary.HoneyKind,
		"hiveCount": apiary.HiveCount,
	}

	return json.Marshal(data)
}

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

	err = command.Validate()
	if err != nil {
		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	apiary, err := apiary_services.CreateApiary(ctx, &command)
	if err != nil {
		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	_, err = apiaryToJson(apiary)
	if err != nil {
		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	web.PrepareSuccessNotification(response, "Apiary created successfully")
	response.WriteHeader(http.StatusOK)

}
