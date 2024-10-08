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
	"html/template"
	"log"
	"net/http"
	"time"

	"github.com/google/uuid"
)

var hiveDetailPageTemplate = template.Must(pages.HtmlPage.ParseFiles("bees/pages/templates/hive_detail.html"))
var CommentDetailTemplate = template.Must(pages.HtmlPage.ParseFiles("bees/pages/templates/comment_detail.html"))

type hiveDetailPageParameter struct {
	Card          components.Card
	CommentDetail commentDetailParameter
}

type commentDetailParameter struct {
	CreateCommentForm components.ModalForm
	Commentaries      components.Table
}

func GetCommentRow(comment *models.Comment) (bytes.Buffer, error) {
	params := components.Row{
		Cells: []components.Cell{
			{Label: comment.Date.Format("%Y-%m-%d")},
			{Label: comment.Type},
			{Label: comment.Body},
		},
	}
	var commentRow bytes.Buffer
	err := pages.HtmlPage.ExecuteTemplate(&commentRow, "table_row.html", &params)
	return commentRow, err
}

func GetHiveDetailBody(ctx context.Context, hivePublicId *uuid.UUID, userId *uuid.UUID) (*bytes.Buffer, error) {
	hive, err := repositories.GetHive(ctx, hivePublicId)
	if err != nil {
		log.Printf("Could not load hive: %s", err)
		return nil, err
	}

	var apiaryName string
	if hive.Apiary != nil {
		apiaryName = hive.Apiary.Name
	}
	params := hiveDetailPageParameter{
		Card: components.Card{
			Header: components.CardHeader{
				Title: hive.Name,
			},
			Content: components.CardContent{
				HorizontalTable: components.HorizontalTable{
					Values: []components.HorizontalTableValue{
						{Key: "Apiculteur", Value: hive.Beekeeper},
						{Key: "Rucher", Value: apiaryName},
						{Key: "Santé de l'essaim", Value: hive.Swarm.Health},
					},
				},
			},
			Footer: components.CardFooter{
				Buttons: []components.Button{
					{Label: "Éditer", Type: "is-ghost"},
					{Label: "Supprimer", Type: "is-ghost"},
				},
			},
		},
		CommentDetail: commentDetailParameter{
			CreateCommentForm: components.ModalForm{
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
					Swap:   "none",
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
					},
				},
			},
			Commentaries: components.Table{
				IsFullWidth: true,
				IsStripped:  true,
				Headers: []components.Header{
					{Label: "Date"},
					{Label: "Type"},
					{Label: "Comment"},
				},
				Rows: []components.Row{
					{
						Cells: []components.Cell{
							{Label: "2024-09-02"},
							{Label: "Nourriture"},
							{Label: "3L avec 1/8Kg sucre"},
						},
					},
					{
						Cells: []components.Cell{
							{Label: "2024-09-01"},
							{Label: "Note"},
							{Label: "Blablabla azheaziej"},
						},
					},
					{
						Cells: []components.Cell{
							{Label: "2024-08-31"},
							{Label: "Note"},
							{Label: "Blablabla azheaziej"},
						},
					},
				},
			},
		},
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
		web.ReturnFullPage(ctx, response, *hiveDetailPage, userId)
	}
}
