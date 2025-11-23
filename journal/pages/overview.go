package pages

import (
	"bytes"
	"context"
	"embed"
	"fmt"
	"html/template"
	"log"

	"akingbee/web/pages"

	"github.com/google/uuid"
)

//go:embed templates/*
var TemplatesFS embed.FS

var overviewTemplate = template.Must(pages.HtmlPage.ParseFS(TemplatesFS, "templates/overview.html"))

func GetOverviewBody(ctx context.Context, userID *uuid.UUID) (*bytes.Buffer, error) {
	var overviewPage bytes.Buffer
	err := pages.HtmlPage.ExecuteTemplate(&overviewPage, "overview.html", nil)

	if err != nil {
		log.Printf("Failed to build overview page: %s", err)

		return nil, fmt.Errorf("failed to build overview: %w", err)
	}

	return &overviewPage, nil
}
