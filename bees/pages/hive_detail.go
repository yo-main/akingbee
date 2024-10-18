package pages

import (
	"akingbee/bees/models"
	"akingbee/bees/repositories"
	"akingbee/internal/htmx"
	"akingbee/user/services"
	"akingbee/web"
	"akingbee/web/components"
	"akingbee/web/pages"
	"bytes"
	"context"
	"fmt"
	"html/template"
	"log"
	"net/http"
	"time"

	"github.com/google/uuid"
)

var hiveDetailPageTemplate = template.Must(pages.HtmlPage.ParseFiles("bees/pages/templates/hive_detail.html"))
var CommentDetailTemplate = template.Must(pages.HtmlPage.ParseFiles("bees/pages/templates/hive_detail_comment.html"))

type hiveDetailPageParameter struct {
	Card          components.Card
	CommentDetail commentDetailParameter
	HivePublicId  *uuid.UUID
}

type commentDetailParameter struct {
	CreateCommentForm components.UpdateStrategy
	Commentaries      components.Table
}

func GetCommentRow(comment *models.Comment) *components.Row {
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
								Url:    fmt.Sprintf("/comment/%s", comment.PublicId),
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
									FormId: fmt.Sprintf("comment-edit-%s", comment.PublicId),
								},
								Form: components.Form{
									Id:     fmt.Sprintf("comment-edit-%s", comment.PublicId),
									Method: "put",
									Url:    fmt.Sprintf("/comment/%s", comment.PublicId),
									Inputs: []components.Input{
										{
											GroupedInput: []components.Input{
												{
													Name:     "type",
													Required: true,
													Narrow:   true,
													ChoicesStrict: []components.Choice{
														{Key: "note", Label: "note"},
														{Key: "feed", Label: "nourriture"},
														{Key: "todo", Label: "action"},
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

func GetHiveDetailCard(ctx context.Context, userId *uuid.UUID, hive *models.Hive) components.Card {
	apiaryName := hive.GetApiaryName()
	apiaries, _ := repositories.GetApiaries(ctx, userId)
	swarmHealths := repositories.GetSwarmValues(ctx, "health", userId)
	beekeepers := repositories.GetHiveValues(ctx, "beekeeper", userId)

	return components.Card{
		Id: "card-hive-detail",
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
							Url:    fmt.Sprintf("/hive/%s", hive.PublicId),
							Method: "delete",
						},
					},
				},
			},
		},
	}
}

func GetCommentSection(ctx context.Context, hive *models.Hive) (*commentDetailParameter, error) {

	comments, err := repositories.GetComments(ctx, &hive.PublicId)
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
					FormId: "create-comment",
					Type:   "is-link",
				},
				Form: components.Form{
					Id:     "create-comment",
					Method: "post",
					Url:    "/comment",
					Inputs: []components.Input{
						{
							GroupedInput: []components.Input{
								{
									Name:     "type",
									Required: true,
									Narrow:   true,
									ChoicesStrict: []components.Choice{
										{Key: "note", Label: "note"},
										{Key: "feed", Label: "nourriture"},
										{Key: "todo", Label: "action"},
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
							Default: hive.PublicId.String(),
						},
					},
				},
			},
		},
		Commentaries: components.Table{
			Id:          "table-hive-comments",
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

func GetHiveDetailBody(ctx context.Context, hivePublicId *uuid.UUID, userId *uuid.UUID) (*bytes.Buffer, error) {
	hive, err := repositories.GetHive(ctx, hivePublicId)
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
		Card:          GetHiveDetailCard(ctx, userId, hive),
		CommentDetail: *commentSection,
		HivePublicId:  &hive.PublicId,
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

	hivePublicId, err := uuid.Parse(req.PathValue("hivePublicId"))
	if err != nil {
		log.Printf("hive id is not an uuid: %s", err)
		response.WriteHeader(http.StatusNotFound)
		return
	}

	userId, err := services.AuthenticateUser(req)

	if err != nil {
		log.Printf("Could not authenticate user: %s", err)
		response.WriteHeader(http.StatusUnauthorized)
		return
	}

	hiveDetailPage, err := GetHiveDetailBody(ctx, &hivePublicId, userId)
	if err != nil {
		log.Printf("Could not get hive detail page: %s", err)
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	if htmx.IsHtmxRequest(req) {
		response.Write(hiveDetailPage.Bytes())
	} else {
		web.ReturnFullPage(ctx, req, response, *hiveDetailPage, userId)
	}
}

func HandleGetHiveComments(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()

	userId, err := services.AuthenticateUser(req)

	if err != nil {
		log.Printf("Could not authenticate user: %s", err)
		web.PrepareFailedNotification(response, "Not authenticated")
		response.WriteHeader(http.StatusUnauthorized)
		return
	}

	hivePublicId, err := uuid.Parse(req.PathValue("hivePublicId"))
	if err != nil {
		log.Printf("The provided hive id is incorrect: %s", err)
		web.PrepareFailedNotification(response, "Not Found")
		response.WriteHeader(http.StatusNotFound)
		return
	}

	hive, err := repositories.GetHive(ctx, &hivePublicId)
	if err != nil {
		web.PrepareFailedNotification(response, "Not Found")
		response.WriteHeader(http.StatusNotFound)
		return
	}

	if hive.User != *userId {
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

	response.Write(body.Bytes())
}
