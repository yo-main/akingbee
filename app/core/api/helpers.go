package api

import (
	"akingbee/app/core/api/templates"
	"encoding/json"
	"log"
	"net/http"
)

func prepareNotification(response http.ResponseWriter, notification *templates.NotificationComponent) {
	html, err := notification.Build()
	if err != nil {
		log.Printf("Could not build notification: %s", err)
	}

	events := map[string]interface{}{
		"notificationEvent": html,
	}
	triggerHeader, _ := json.Marshal(events)
	response.Header().Set("HX-Trigger", string(triggerHeader))
}

func PrepareFailedNotification(response http.ResponseWriter, msg string) {
	notification := templates.NotificationComponent{
		Type:    "danger",
		Content: msg,
	}

	prepareNotification(response, &notification)
}

func PrepareSuccessNotification(response http.ResponseWriter, msg string) {
	notification := templates.NotificationComponent{
		Type:    "success",
		Content: msg,
	}
	prepareNotification(response, &notification)
}
