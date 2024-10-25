package web

import (
	"github.com/google/uuid"
	"net/http"
)

type Request struct {
	UserId          *uuid.UUID
	OriginalRequest *http.Request
}
