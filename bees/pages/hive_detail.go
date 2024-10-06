package pages

import (
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

	"github.com/google/uuid"
)

var hiveDetailPageTemplate = template.Must(pages.HtmlPage.ParseFiles("bees/pages/templates/hive_detail.html"))

type hiveDetailPageParameter struct {
	Card         components.Card
	Commentaries components.Table
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
