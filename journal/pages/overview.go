package pages

import (
	"bytes"
	"context"
	"embed"
	"fmt"
	"html/template"
	"log"
	"time"

	"akingbee/journal/models"
	"akingbee/journal/repositories"
	"akingbee/web/components"
	"akingbee/web/pages"

	"github.com/google/uuid"
)

//go:embed templates/*
var TemplatesFS embed.FS

var overviewTemplate = template.Must(pages.HtmlPage.ParseFS(TemplatesFS, "templates/overview.html"))

type ApiaryParam struct {
	Apiary            models.ApiaryWithComment
	CreateCommentForm components.UpdateStrategy
}
type OverviewPageParameter struct {
	Apiaries []ApiaryParam
}

func GetOverviewBody(ctx context.Context, userID *uuid.UUID) (*bytes.Buffer, error) {
	var overviewPage bytes.Buffer

	apiaries, err := repositories.ListApiariesWithComment(ctx, userID)
	if err != nil {
		log.Printf("Failed to list apiaries: %s", err)

		return nil, fmt.Errorf("failed to build overview: %w", err)
	}

	apiaryParams := make([]ApiaryParam, len(apiaries))

	for i, apiary := range apiaries {
		apiaryParams[i] = ApiaryParam{
			Apiary: apiary,
			CreateCommentForm: components.UpdateStrategy{
				Target: fmt.Sprintf("#apiary-%s-comment-body", apiary.ApiaryPublicID.String()),
				Swap:   "afterbegin",
				Modal: &components.ModalForm{
					Title: "Nouveau commentaire",
					ShowModalButton: components.Button{
						Label: "Nouveau commentaire",
					},
					SubmitFormButton: components.Button{
						Label:  "Nouveau",
						FormID: fmt.Sprintf("apiary-%s-comment-create", apiary.ApiaryPublicID.String()),
						Type:   "is-link",
					},
					Form: components.Form{
						ID:     fmt.Sprintf("apiary-%s-comment-create", apiary.ApiaryPublicID.String()),
						Method: "post",
						URL:    "/comment",
						Inputs: []components.Input{
							{
								GroupedInput: []components.Input{
									{
										Name:     "type",
										Required: true,
										Narrow:   true,
										ChoicesStrict: []components.Choice{
											{Key: "note", Label: "note"},
											{Key: "nourriture", Label: "nourriture"},
											{Key: "action", Label: "action"},
										},
									},
									{
										Name:     "date",
										Required: true,
										Type:     "date",
										Default:  time.Now().Format("2006-01-02"),
									},
								},
							},
							{
								Name:       "body",
								Required:   true,
								RichEditor: true,
							},
							{
								Name:    "apiary_id",
								Type:    "hidden",
								Default: apiary.ApiaryPublicID.String(),
							},
						},
					},
				},
			}}
	}

	params := OverviewPageParameter{
		Apiaries: apiaryParams,
	}

	err = pages.HtmlPage.ExecuteTemplate(&overviewPage, "overview.html", &params)

	if err != nil {
		log.Printf("Failed to build overview page: %s", err)

		return nil, fmt.Errorf("failed to build overview: %w", err)
	}

	return &overviewPage, nil
}
