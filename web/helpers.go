package web

import (
	user_services "akingbee/user/services"
	"akingbee/web/components"
	"akingbee/web/pages"
	"bytes"
	"context"
	"encoding/json"
	"github.com/google/uuid"
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

func ReturnFullPage(ctx context.Context, response http.ResponseWriter, content bytes.Buffer, userId *uuid.UUID) {
	var menu *bytes.Buffer
	var err error

	if userId != nil {
		user, err := user_services.GetUser(ctx, userId)
		if err != nil {
			log.Printf("User not found: %s", err)
			return
		}

		menu, err = components.GetLoggedInMenu(user.Credentials.Username)
		if err != nil {
			log.Printf("Could not get logged in menu: %s", err)
			return
		}
	} else {
		menu, err = components.GetLoggedOutMenu()
		if err != nil {
			log.Printf("Could not build logged out menu: %s", err)
			return
		}
	}

	page, err := pages.BuildPage(pages.GetBody(template.HTML(content.Bytes()), template.HTML(menu.Bytes())))
	if err != nil {
		log.Printf("Could not buiild full page: %s", err)
		return
	}

	response.Write([]byte(page))

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

func PrepareLoggedInMenu(response http.ResponseWriter, username string) {
	menu, err := components.GetLoggedInMenu(username)
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