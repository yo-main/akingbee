package web

import (
	"bytes"
	"context"
	"html/template"
	"log"
	"net/http"

	user_models "akingbee/user/models"
	"akingbee/web/components"
	"akingbee/web/pages"
	"encoding/json"
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
	triggerHeader, err := json.Marshal(events)

	if err != nil {
		log.Println("Error when converting events to json: %w", err)

		return
	}

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
	triggerHeader, err := json.Marshal(events)

	if err != nil {
		log.Println("Error when converting events to json: %w", err)

		return
	}

	response.Header().Set("HX-Trigger-After-Swap", string(triggerHeader))
}

func PrepareLoggedInMenu(req *http.Request, response http.ResponseWriter, user *user_models.AuthenticatedUser) {
	menu, err := components.GetLoggedInMenu(user, req.URL.Path)
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

func ReturnFullPage(_ context.Context, req *http.Request, _ http.ResponseWriter, content []byte) []byte {
	menu, err := GetMenu(req)
	if err != nil {
		log.Printf("Could not get menu: %s", err)

		return content
	}

	page, err := pages.BuildPage(pages.GetBody(template.HTML(content), template.HTML(menu.Bytes())))
	if err != nil {
		log.Printf("Could not build full page: %s", err)

		return content
	}

	return page
}

func GetMenu(req *http.Request) (*bytes.Buffer, error) {
	ctx := req.Context()

	user, ok := ctx.Value("authenticatedUser").(*user_models.AuthenticatedUser)

	if ok {
		return components.GetLoggedInMenu(user, req.URL.Path)
	}

	return components.GetLoggedOutMenu()
}
