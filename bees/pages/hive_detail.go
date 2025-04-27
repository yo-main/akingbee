package pages

import (
	"bytes"
	"context"
	"fmt"
	"html/template"
	"log"
	"net/http"
	"time"

	models_bees "akingbee/bees/models"
	repositories_bees "akingbee/bees/repositories"
	api_helpers "akingbee/internal/web"
	models_journal "akingbee/journal/models"
	repositories_journal "akingbee/journal/repositories"
	models_user "akingbee/user/models"
	"akingbee/web"
	"akingbee/web/components"
	"akingbee/web/pages"

	"github.com/google/uuid"
)

var hiveDetailPageTemplate = template.Must(pages.HtmlPage.ParseFS(TemplatesFS, "templates/hive_detail.html"))
var CommentDetailTemplate = template.Must(pages.HtmlPage.ParseFS(TemplatesFS, "templates/hive_detail_comment.html"))

type hiveDetailPageParameter struct {
	Card          components.Card
	CommentDetail commentDetailParameter
	HivePublicID  *uuid.UUID
}

type commentDetailParameter struct {
	CreateCommentForm components.UpdateStrategy
	Commentaries      components.Table
}

func GetCommentRow(comment *models_journal.Comment) *components.Row {
	params := components.Row{
		Cells: []components.Cell{
			{
				GroupedCells: []components.Cell{
					{
						UpdateStrategy: &components.UpdateStrategy{
							Swap:    "delete",
							Target:  "closest tr",
							Confirm: "Supprimer le commentaire ?",
							Button: &components.Button{
								Icon:   "delete",
								URL:    fmt.Sprintf("/comment/%s", comment.PublicID),
								Method: "delete",
							},
						},
					},
					{
						UpdateStrategy: &components.UpdateStrategy{
							Swap:   "outerHTML",
							Target: "closest tr",
							Modal: &components.ModalForm{
								Title: "Editer le commentaire",
								ShowModalButton: components.Button{
									Icon: "edit",
								},
								SubmitFormButton: components.Button{
									Label:  "Sauvegarder",
									Type:   "is-link",
									FormID: fmt.Sprintf("comment-edit-%s", comment.PublicID),
								},
								Form: components.Form{
									ID:     fmt.Sprintf("comment-edit-%s", comment.PublicID),
									Method: "put",
									URL:    fmt.Sprintf("/comment/%s", comment.PublicID),
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
													Default: comment.Type,
												},
												{
													Name:     "date",
													Required: true,
													Type:     "date",
													Default:  comment.Date.Format("2006-01-02"),
												},
											},
										},
										{
											Name:       "body",
											Required:   true,
											RichEditor: true,
											Default:    comment.Body,
										},
									},
								},
							},
						},
					},
				},
			},
			{Label: comment.Date.Format("2006-01-02")},
			{Label: comment.Type},
			{HTMLContent: template.HTML(fmt.Sprintf("<div class=\"content\">%s</div>", comment.Body))},
		},
	}

	return &params
}

func GetHiveDetailCard(ctx context.Context, userID *uuid.UUID, hive *models_bees.Hive) components.Card {
	apiaryName := hive.GetApiaryName()
	apiaries, _ := repositories_bees.GetApiaries(ctx, userID)
	swarmHealths := repositories_bees.GetSwarmValues(ctx, "health", userID)
	beekeepers := repositories_bees.GetHiveValues(ctx, "beekeeper", userID)

	return components.Card{
		ID: "card-hive-detail",
		Header: components.CardHeader{
			Title: hive.Name,
		},
		Content: components.CardContent{
			HorizontalTable: components.HorizontalTable{
				Values: []components.HorizontalTableValue{
					{Key: "Apiculteur", Value: hive.Beekeeper},
					{Key: "Rucher", Value: apiaryName},
					{Key: "Santé de l'essaim", Value: hive.GetSwarmHealth()},
				},
			},
		},
		Footer: components.CardFooter{
			Items: []components.CardFooterItem{
				{
					UpdateStrategy: EditHiveModal(
						hive,
						GetApiariesChoices(apiaries, hive),
						GetSwarmHealthChoices(swarmHealths, hive),
						GetBeekeeperChoices(beekeepers, hive),
						components.Button{
							Label: "Éditer",
							Type:  "is-ghost",
						},
						"#card-hive-detail",
						"innerHTML",
						"card",
					),
				},
				{
					UpdateStrategy: &components.UpdateStrategy{
						Confirm: "Supprimer la ruche ?",
						AdditionalValue: `{
							"redirectTo": "/hive"
						}`,
						Button: &components.Button{
							Label:  "Supprimer",
							Type:   "is-ghost",
							URL:    fmt.Sprintf("/hive/%s", hive.PublicID),
							Method: "delete",
						},
					},
				},
			},
		},
	}
}

func GetCommentSection(ctx context.Context, hive *models_bees.Hive) (*commentDetailParameter, error) {

	comments, err := repositories_journal.GetComments(ctx, &hive.PublicID)
	if err != nil {
		log.Printf("Could not get comments: %s", err)
		return nil, err
	}

	var commentRows []components.Row
	for _, comment := range comments {
		commentRows = append(commentRows, *GetCommentRow(&comment))
	}

	params := commentDetailParameter{
		CreateCommentForm: components.UpdateStrategy{
			Target: "#table-hive-comments",
			Swap:   "afterbegin",
			Modal: &components.ModalForm{
				Title: "Nouveau commentaire",
				ShowModalButton: components.Button{
					Label: "Nouveau commentaire",
				},
				SubmitFormButton: components.Button{
					Label:  "Créer",
					FormID: "create-comment",
					Type:   "is-link",
				},
				Form: components.Form{
					ID:     "create-comment",
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
							Name:    "hive_id",
							Type:    "hidden",
							Default: hive.PublicID.String(),
						},
					},
				},
			},
		},
		Commentaries: components.Table{
			ID:          "table-hive-comments",
			IsFullWidth: true,
			IsStripped:  true,
			Headers: []components.Header{
				{Label: "Actions"},
				{Label: "Date"},
				{Label: "Type"},
				{Label: "Comment"},
			},
			ColumnSizes: []components.ColumnSize{
				{Span: "1", Style: "width: 10%"},
				{Span: "1", Style: "width: 10%"},
				{Span: "1", Style: "width: 10%"},
				{Span: "1", Style: "width: 70%"},
			},
			Rows: commentRows,
		},
	}

	return &params, nil
}

func GetHiveDetailBody(ctx context.Context, hivePublicID *uuid.UUID, userID *uuid.UUID) (*bytes.Buffer, error) {
	hive, err := repositories_bees.GetHive(ctx, hivePublicID)
	if err != nil {
		log.Printf("Could not load hive: %s", err)
		return nil, err
	}

	commentSection, err := GetCommentSection(ctx, hive)
	if err != nil {
		log.Printf("Could not load comment section: %s", err)
		return nil, err
	}

	params := hiveDetailPageParameter{
		Card:          GetHiveDetailCard(ctx, userID, hive),
		CommentDetail: *commentSection,
		HivePublicID:  &hive.PublicID,
	}

	var hiveDetailPage bytes.Buffer
	err = pages.HtmlPage.ExecuteTemplate(&hiveDetailPage, "hive_detail.html", &params)

	if err != nil {
		log.Printf("Failed to build hive detail page: %s", err)
		return nil, err
	}

	return &hiveDetailPage, nil
}

func HandleGetHiveDetail(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()

	hivePublicID, err := uuid.Parse(req.PathValue("hivePublicId"))
	if err != nil {
		log.Printf("hive id is not an uuid: %s", err)
		response.WriteHeader(http.StatusNotFound)

		return
	}

	if user, ok := ctx.Value("authenticatedUser").(*models_user.AuthenticatedUser); ok {
		hiveDetailPage, err := GetHiveDetailBody(ctx, &hivePublicID, &user.PublicID)
		if err != nil {
			log.Printf("Could not get hive detail page: %s", err)
			response.WriteHeader(http.StatusBadRequest)

			return
		}

		api_helpers.WriteToResponse(response, hiveDetailPage.Bytes())
	} else {
		panic("unreacheable")
	}
}

func HandleGetHiveComments(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()

	hivePublicID, err := uuid.Parse(req.PathValue("hivePublicId"))
	if err != nil {
		log.Printf("The provided hive id is incorrect: %s", err)
		web.PrepareFailedNotification(response, "Not Found")
		response.WriteHeader(http.StatusNotFound)

		return
	}

	hive, err := repositories_bees.GetHive(ctx, &hivePublicID)
	if err != nil {
		web.PrepareFailedNotification(response, "Not Found")
		response.WriteHeader(http.StatusNotFound)

		return
	}

	if user, ok := ctx.Value("authenticatedUser").(*models_user.AuthenticatedUser); ok {
		if hive.User != user.PublicID {
			web.PrepareFailedNotification(response, "Forbidden")
			response.WriteHeader(http.StatusForbidden)

			return
		}

		commentSection, err := GetCommentSection(ctx, hive)
		if err != nil {
			web.PrepareFailedNotification(response, "Could not get comment section")
			response.WriteHeader(http.StatusBadRequest)

			return
		}

		var body bytes.Buffer
		err = pages.HtmlPage.ExecuteTemplate(&body, "hive_detail_comment.html", &commentSection)

		if err != nil {
			web.PrepareFailedNotification(response, "Could not build comment section")
			response.WriteHeader(http.StatusBadRequest)

			return
		}

		api_helpers.WriteToResponse(response, body.Bytes())
	} else {
		panic("unreacheable")
	}
}
