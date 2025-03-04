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
		userID, err := user_services.AuthenticateUser(req)

		if err != nil {
			log.Printf("Could not authenticate user: %s", err)
			response.WriteHeader(http.StatusUnauthorized)
			return
		}

		user, err := user_services.GetUser(req.Context(), userID)
		if err != nil {
			log.Printf("User %s not found: %s", userID, err)
			response.WriteHeader(http.StatusUnauthorized)
			return
		}

		callback(response, req.WithContext(context.WithValue(req.Context(), "authenticatedUser", user)))
	}
}

func AuthenticatedAsAdmin(callback func(response http.ResponseWriter, req *http.Request)) func(response http.ResponseWriter, req *http.Request) {

	return func(response http.ResponseWriter, req *http.Request) {
		userID, err := user_services.AuthenticateUser(req)

		if err != nil {
			log.Printf("Could not authenticate user: %s", err)
			response.WriteHeader(http.StatusUnauthorized)
			return
		}

		user, err := user_services.GetUser(req.Context(), userID)
		if err != nil {
			log.Printf("User %s not found: %s", userID, err)
			response.WriteHeader(http.StatusUnauthorized)
			return
		}

		callback(response, req.WithContext(context.WithValue(req.Context(), "authenticatedUser", user)))
	}
}

func OptionallyAuthenticated(callback func(response http.ResponseWriter, req *http.Request)) func(response http.ResponseWriter, req *http.Request) {

	return func(response http.ResponseWriter, req *http.Request) {
		userID, err := user_services.AuthenticateUser(req)

		if err == nil {
			user, err := user_services.GetUser(req.Context(), userID)
			if err != nil {
				log.Printf("User %s not found: %s", userID, err)
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
			response.Write(web.ReturnFullPage(req.Context(), req, response, wrappedResponse.GetBody()))
		} else {
			response.Write(wrappedResponse.GetBody())
		}
	}
}

func HandleNotFound(response http.ResponseWriter, req *http.Request) {
	response.Write(pages.GetNotFoundContent().Bytes())
}
