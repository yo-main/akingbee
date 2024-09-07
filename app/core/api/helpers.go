package api

import (
	"akingbee/app/core/api/templates"
	"encoding/json"
	"net/http"
)

func prepareNotification(response *http.ResponseWriter, msg string) {
	events := map[string]interface{}{
		"notificationEvent": msg,
	}
	triggerHeader, _ := json.Marshal(events)
	(*response).Header().Set("HX-Trigger", string(triggerHeader))
}

func PrepareFailedNotification(response *http.ResponseWriter, msg string) {
	prepareNotification(response, templates.BuildErrorNotification(msg))
}

func PrepareSuccessNotification(response *http.ResponseWriter, msg string) {
	prepareNotification(response, templates.BuildSuccessNotification(msg))
}
