package web

import (
	"net/http"
)

type Response struct {
	body             []byte
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
	response.originalResponse.WriteHeader(statusCode)
}

func (response *Response) GetBody() []byte {
	return response.body
}
