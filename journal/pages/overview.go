package pages

import (
	"bytes"
	"context"
	"embed"
	"fmt"
	"html/template"
	"log"

	"akingbee/journal/models"
	"akingbee/journal/repositories"
	"akingbee/web/pages"

	"github.com/google/uuid"
)

//go:embed templates/*
var TemplatesFS embed.FS

var overviewTemplate = template.Must(pages.HtmlPage.ParseFS(TemplatesFS, "templates/overview.html"))

type OverviewPageParameter struct {
	Apiaries []models.ApiaryWithComment
}

func GetOverviewBody(ctx context.Context, userID *uuid.UUID) (*bytes.Buffer, error) {
	var overviewPage bytes.Buffer

	apiaries, err := repositories.ListApiariesWithComment(ctx, userID)
	if err != nil {
		log.Printf("Failed to list apiaries: %s", err)

		return nil, fmt.Errorf("failed to build overview: %w", err)
	}

	params := OverviewPageParameter{
		Apiaries: apiaries,
	}

	err = pages.HtmlPage.ExecuteTemplate(&overviewPage, "overview.html", &params)

	if err != nil {
		log.Printf("Failed to build overview page: %s", err)

		return nil, fmt.Errorf("failed to build overview: %w", err)
	}

	return &overviewPage, nil
}
