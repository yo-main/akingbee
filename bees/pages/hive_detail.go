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
	Card components.Card
}

func GetHiveDetailBody(ctx context.Context, hivePublicId *uuid.UUID, userId *uuid.UUID) (*bytes.Buffer, error) {
	hive, err := repositories.GetHive(ctx, hivePublicId)
	if err != nil {
		log.Printf("Could not load hive: %s", err)
		return nil, err
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
						{Key: "Rucher", Value: hive.Apiary.Name},
						{Key: "Santé de l'essaim", Value: hive.Swarm.Health},
					},
				},
			},
			Footer: components.CardFooter{
				Buttons: []components.Button{
					{Label: "Éditer"},
					{Label: "Supprimer"},
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
