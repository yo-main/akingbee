package web

import (
	"net/http"

	"github.com/google/uuid"
)

type Request struct {
	UserID          *uuid.UUID
	OriginalRequest *http.Request
}
