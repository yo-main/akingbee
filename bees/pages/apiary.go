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
	"fmt"
	"html/template"
	"log"
	"net/http"
	"strconv"

	"github.com/google/uuid"
)

var apiaryPageTemplate = template.Must(pages.HtmlPage.ParseFiles("bees/pages/templates/apiary.html"))

type apiaryPageParameter struct {
	CreateApiaryModal components.ModalForm
	Table             components.Table
}

func GetApiaryBody(ctx context.Context, userId *uuid.UUID) (*bytes.Buffer, error) {
	apiaries, err := repositories.GetApiaries(ctx, userId)
	if err != nil {
		log.Printf("Could not get apiaries: %s", err)
		return nil, err
	}

	rows := []components.Rows{}
	for _, apiary := range apiaries {
		rows = append(rows, components.Rows{
			Values: []components.Value{
				{Label: apiary.Name},
				{Label: apiary.Location},
				{Label: apiary.HoneyKind},
				{Label: strconv.Itoa(apiary.HiveCount)},
				{
					ModalForm: components.ModalForm{
						Title:            "Editer le rucher",
						ShowModalButton:  components.Button{Icon: "edit"},
						SubmitFormButton: components.Button{Label: "Sauvegarder"},
						Form: components.Form{
							Id:     fmt.Sprintf("apiary-edit-%s", apiary.Name),
							Method: "put",
							Target: fmt.Sprintf("/apiary/%s", apiary.PublicId),
							Swap:   "none",
							Inputs: []components.Input{
								{
									Name:     "name",
									Label:    "Nom",
									Type:     "text",
									Required: true,
									Default:  apiary.Name,
								},
								{
									Name:     "location",
									Label:    "Lieu",
									Type:     "text",
									Required: true,
									Default:  apiary.Location,
								},
								{
									Name:     "honeyKind",
									Label:    "Type de miel",
									Type:     "text",
									Required: true,
									Default:  apiary.HoneyKind,
								},
							},
						},
					},
				},
			},
		})

	}
	locations := repositories.GetApiaryValues(ctx, "location", userId)
	honeyKind := repositories.GetApiaryValues(ctx, "honey_kind", userId)

	params := apiaryPageParameter{
		CreateApiaryModal: components.ModalForm{
			Title: "Création un nouveau rucher",
			ShowModalButton: components.Button{
				Label: "Nouveau rucher"},
			SubmitFormButton: components.Button{Label: "Créer"},
			Form: components.Form{
				Id:     "createApiary",
				Method: "post",
				Target: "/apiary",
				Swap:   "none",
				Inputs: []components.Input{
					{
						Name:     "name",
						Label:    "Nom",
						Type:     "text",
						Required: true,
					},
					{
						Name:     "location",
						Label:    "Location",
						Type:     "text",
						Required: true,
						Choices:  locations,
					},
					{
						Name:     "honeyKind",
						Label:    "Type de miel",
						Type:     "text",
						Required: true,
						Choices:  honeyKind,
					},
				},
			},
		},
		Table: components.Table{
			IsBordered:  false,
			IsStripped:  true,
			IsFullWidth: true,
			Headers: []components.Header{
				{Label: "Nom"},
				{Label: "Lieu"},
				{Label: "Type de miel"},
				{Label: "Nombre de ruches"},
				{Label: "Actions"},
			},
			Rows: rows,
		}}

	var apiaryPage bytes.Buffer
	err = pages.HtmlPage.ExecuteTemplate(&apiaryPage, "apiary.html", params)

	if err != nil {
		log.Printf("Failed to build apiary page: %s", err)
		return nil, err
	}

	return &apiaryPage, nil

}

func HandleGetApiary(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()

	userId, err := services.AuthenticateUser(req)

	if err != nil {
		log.Printf("Could not authenticate user: %s", err)
		response.WriteHeader(http.StatusUnauthorized)
		return
	}

	apiaryPage, err := GetApiaryBody(ctx, userId)
	if err != nil {
		log.Printf("Could not get apiry page: %s", err)
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	if htmx.IsHtmxRequest(req) {
		response.Write(apiaryPage.Bytes())
	} else {
		web.ReturnFullPage(ctx, response, *apiaryPage, userId)
	}
}
