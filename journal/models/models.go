package models

import (
	"html/template"
	"time"

	"github.com/google/uuid"
)

type Comment struct {
	PublicID       uuid.UUID
	Date           time.Time
	Type           string
	Body           string
	HivePublicID   *uuid.UUID
	ApiaryPublicID *uuid.UUID
}

type ApiaryWithComment struct {
	CommentPublicId *uuid.UUID
	CommentDate     *time.Time
	CommentBody     template.HTML
	CommentType     string
	ApiaryName      string
	ApiaryPublicID  uuid.UUID
	ApiaryUser      uuid.UUID
}
