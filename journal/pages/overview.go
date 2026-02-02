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
var overviewCardTemplate = template.Must(pages.HtmlPage.ParseFS(TemplatesFS, "templates/overview_card.html"))

type ApiaryParam struct {
	Apiary            models.ApiaryWithComment
	CreateCommentForm components.UpdateStrategy
	EditCommentForm   *components.UpdateStrategy
}
type OverviewPageParameter struct {
	Apiaries []ApiaryParam
}

func getApiaryCardForm(apiary *models.ApiaryWithComment) *ApiaryParam {
	// Build edit form if comment exists
	var editForm *components.UpdateStrategy
	if apiary.CommentPublicId != nil {
		editForm = &components.UpdateStrategy{
			Target: fmt.Sprintf("#apiary-%s-card", apiary.ApiaryPublicID.String()),
			Swap:   "outerHTML",
			Modal: &components.ModalForm{
				Title: "Editer le commentaire",
				ShowModalButton: components.Button{
					Label: "Editer",
				},
				SubmitFormButton: components.Button{
					Label:  "Sauvegarder",
					FormID: fmt.Sprintf("apiary-%s-comment-edit", apiary.ApiaryPublicID.String()),
					Type:   "is-link",
				},
				Form: components.Form{
					ID:     fmt.Sprintf("apiary-%s-comment-edit", apiary.ApiaryPublicID.String()),
					Method: "put",
					URL:    fmt.Sprintf("/apiary/%s/comment/%s", apiary.ApiaryPublicID.String(), apiary.CommentPublicId.String()),
					Inputs: []components.Input{
						{
							Name:     "type",
							Required: true,
							Narrow:   true,
							Hidden:   true,
							Default:  apiary.CommentType,
						},
						{
							Name:     "date",
							Required: true,
							Type:     "date",
							Default:  apiary.CommentDate.Format("2006-01-02"),
							Hidden:   true,
						},
						{
							Name:       "body",
							Required:   true,
							RichEditor: true,
							Default:    string(apiary.CommentBody),
						},
					},
				},
			},
		}
	}

	// Build card parameter
	cardParam := ApiaryParam{
		Apiary: *apiary,
		CreateCommentForm: components.UpdateStrategy{
			Target: fmt.Sprintf("#apiary-%s-card", apiary.ApiaryPublicID.String()),
			Swap:   "outerHTML",
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
							Name:     "type",
							Required: true,
							Narrow:   true,
							Default:  "note",
							Hidden:   true,
						},
						{
							Name:     "date",
							Required: true,
							Type:     "date",
							Default:  time.Now().Format("2006-01-02"),
							Hidden:   true,
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
		},
		EditCommentForm: editForm,
	}

	return &cardParam
}

func GetApiaryCard(ctx context.Context, apiaryPublicID *uuid.UUID, userID *uuid.UUID) (*bytes.Buffer, error) {
	var buffer bytes.Buffer

	apiary, err := repositories.GetApiaryWithComment(ctx, apiaryPublicID, userID)
	if err != nil {
		log.Printf("Failed to get apiary: %s", err)
		return nil, fmt.Errorf("failed to get apiary: %w", err)
	}

	// Fetch apiary with its most recent comment
	cardParam := getApiaryCardForm(apiary)

	err = pages.HtmlPage.ExecuteTemplate(&buffer, "overview_card.html", cardParam)
	if err != nil {
		log.Printf("Failed to build card: %s", err)
		return nil, fmt.Errorf("failed to build card: %w", err)
	}

	return &buffer, nil
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
		cardForm := getApiaryCardForm(&apiary)
		apiaryParams[i] = *cardForm
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
