package web

import (
	"akingbee/web/components"
	"bytes"
	"encoding/json"
	"html/template"
	"log"
	"net/http"
)

func getEventMap(response http.ResponseWriter, headerKey string) map[string]interface{} {
	var events map[string]interface{}

	headerValue := response.Header().Get(headerKey)
	if headerValue != "" {
		err := json.Unmarshal([]byte(headerValue), &events)
		if err != nil {
			log.Printf("Error while unparsing header %s: %s", headerKey, err)
			return map[string]interface{}{}
		}

	} else {
		events = map[string]interface{}{}
	}

	return events
}

func prepareNotification(response http.ResponseWriter, notification *components.NotificationComponent) {
	html, err := notification.Build()
	if err != nil {
		log.Printf("Could not build notification: %s", err)
		return
	}

	var headerKey string
	if notification.Type == "success" {
		headerKey = "HX-Trigger-After-Swap"
	} else {
		headerKey = "HX-Trigger"
	}

	events := getEventMap(response, headerKey)

	events["notificationEvent"] = html
	triggerHeader, _ := json.Marshal(events)

	if notification.Type == "success" {
		response.Header().Set("HX-Trigger-After-Swap", string(triggerHeader))
	} else {
		response.Header().Set("HX-Trigger", string(triggerHeader))
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

func prepareMenuEvent(response http.ResponseWriter, menu *bytes.Buffer) {
	events := getEventMap(response, "HX-Trigger-After-Swap")

	events["menuEvent"] = template.HTML(menu.String())
	triggerHeader, _ := json.Marshal(events)

	response.Header().Set("HX-Trigger-After-Swap", string(triggerHeader))
}

func PrepareLoggedInMenu(response http.ResponseWriter) {
	menu, err := components.GetLoggedInMenu()
	if err != nil {
		log.Printf("Could not generate menu: %s", err)
		return
	}

	prepareMenuEvent(response, menu)
}

func PrepareLoggedOutMenu(response http.ResponseWriter) {
	menu, err := components.GetLoggedOutMenu()
	if err != nil {
		log.Printf("Could not generate menu: %s", err)
		return
	}

	prepareMenuEvent(response, menu)
}
