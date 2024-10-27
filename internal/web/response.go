package web

import (
	"akingbee/internal/web/pages"
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
