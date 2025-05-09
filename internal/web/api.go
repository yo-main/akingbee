package web

import (
	"context"
	"log"
	"net/http"

	"akingbee/internal/htmx"
	"akingbee/internal/web/pages"
	user_services "akingbee/user/services"
	"akingbee/web"
)

func Authenticated(callback func(response http.ResponseWriter, req *http.Request)) func(response http.ResponseWriter, req *http.Request) {

	return func(response http.ResponseWriter, req *http.Request) {
		loggedUser, err := user_services.AuthenticateUser(req)

		if err != nil {
			log.Printf("Could not authenticate user: %s", err)
			response.WriteHeader(http.StatusUnauthorized)
			return
		}

		callback(response, req.WithContext(context.WithValue(req.Context(), "authenticatedUser", loggedUser)))
	}
}

func AuthenticatedAsAdmin(callback func(response http.ResponseWriter, req *http.Request)) func(response http.ResponseWriter, req *http.Request) {

	return func(response http.ResponseWriter, req *http.Request) {
		loggedUser, err := user_services.AuthenticateUser(req)

		if err != nil {
			log.Printf("Could not authenticate user: %s", err)
			response.WriteHeader(http.StatusUnauthorized)
			return
		}

		user, err := user_services.GetUser(req.Context(), &loggedUser.PublicID)
		if err != nil {
			log.Printf("User %s not found: %s", loggedUser.PublicID, err)
			response.WriteHeader(http.StatusUnauthorized)

			return
		}

		callback(response, req.WithContext(context.WithValue(req.Context(), "authenticatedUser", user)))
	}
}

func OptionallyAuthenticated(callback func(response http.ResponseWriter, req *http.Request)) func(response http.ResponseWriter, req *http.Request) {

	return func(response http.ResponseWriter, req *http.Request) {
		loggedUser, err := user_services.AuthenticateUser(req)

		if err == nil {
			user, err := user_services.GetUser(req.Context(), &loggedUser.PublicID)
			if err != nil {
				log.Printf("User %s not found: %s", loggedUser.PublicID, err)
				response.WriteHeader(http.StatusUnauthorized)

				return
			}

			req = req.WithContext(context.WithValue(req.Context(), "authenticatedUser", user))
		}

		callback(response, req)

	}
}

func HtmxMiddleware(callback func(response http.ResponseWriter, req *http.Request)) func(response http.ResponseWriter, req *http.Request) {

	return func(response http.ResponseWriter, req *http.Request) {
		wrappedResponse := Response{
			originalResponse: response,
		}

		callback(&wrappedResponse, req)

		if !htmx.IsHtmxRequest(req) {
			WriteToResponse(response, web.ReturnFullPage(req.Context(), req, response, wrappedResponse.GetBody()))
		} else {
			WriteToResponse(response, wrappedResponse.GetBody())
		}
	}
}

func HandleNotFound(response http.ResponseWriter, req *http.Request) {
	WriteToResponse(response, pages.GetNotFoundContent().Bytes())
	response.WriteHeader(http.StatusNotFound)
}
