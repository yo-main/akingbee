package web

import (
	"akingbee/internal/web/pages"
	"log"
	"net/http"
)

type Response struct {
	body             []byte
	statusCode       int
	originalResponse http.ResponseWriter
}

func (response *Response) Header() http.Header {
	return response.originalResponse.Header()
}

func (response *Response) Write(body []byte) (int, error) {
	response.body = body
	return len(body), nil
}

func (response *Response) WriteHeader(statusCode int) {
	response.statusCode = statusCode
	response.originalResponse.WriteHeader(statusCode)
}

func (response *Response) GetBody() []byte {
	if response.statusCode == http.StatusNotFound {
		return pages.GetNotFoundContent().Bytes()
	}

	return response.body
}

func WriteToResponse(response http.ResponseWriter, bytes []byte) {
	_, err := response.Write(bytes)

	if err != nil {
		log.Println("Failed to write to response: %w", err)
	}
}
