package web

import (
	"akingbee/web/components"
	"encoding/json"
	"html/template"
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

	if notification.Type == "success" {
		response.Header().Add("HX-Trigger-After-Swap", string(triggerHeader))
	} else {
		response.Header().Add("HX-Trigger", string(triggerHeader))
	}
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

func PrepareLoggedInMenu(response http.ResponseWriter) {
	menu, err := components.GetLoggedInMenu()
	if err != nil {
		log.Printf("Could not generate menu: %s", err)
		return
	}

	events := map[string]interface{}{
		"menuEvent": template.HTML(menu.String()),
	}
	triggerHeader, _ := json.Marshal(events)

	response.Header().Add("HX-Trigger-After-Swap", string(triggerHeader))
}

func PrepareLoggedOutMenu(response http.ResponseWriter) {
	menu, err := components.GetLoggedOutMenu()
	if err != nil {
		log.Printf("Could not generate menu: %s", err)
		return
	}

	events := map[string]interface{}{
		"menuEvent": template.HTML(menu.String()),
	}
	triggerHeader, _ := json.Marshal(events)

	response.Header().Add("HX-Trigger-After-Swap", string(triggerHeader))
}
