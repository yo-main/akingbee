package web

import (
	"akingbee/web/components"
	"encoding/json"
	"log"
	"net/http"
)

func prepareNotification(response http.ResponseWriter, notification *components.NotificationComponent) {
	html, err := notification.Build()
	if err != nil {
		log.Printf("Could not build notification: %s", err)
	}

	events := map[string]interface{}{
		"notificationEvent": html,
	}
	triggerHeader, _ := json.Marshal(events)
	response.Header().Set("HX-Trigger-After-Swap", string(triggerHeader))
}

func PrepareFailedNotification(response http.ResponseWriter, msg string) {
	notification := components.NotificationComponent{
		Type:    "danger",
		Content: msg,
	}

	prepareNotification(response, &notification)
}

func PrepareSuccessNotification(response http.ResponseWriter, msg string) {
	notification := components.NotificationComponent{
		Type:    "success",
		Content: msg,
	}
	prepareNotification(response, &notification)
}
