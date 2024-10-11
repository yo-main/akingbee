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
	"github.com/google/uuid"
	"html/template"
	"log"
	"net/http"
	"strconv"
)

var apiaryPageTemplate = template.Must(pages.HtmlPage.ParseFiles("bees/pages/templates/apiary.html"))

type apiaryPageParameter struct {
	CreateApiaryModal components.ModalForm
	Table             components.Table
}

func GetApiaryTableRow(apiary *models.Apiary) components.Row {
	return components.Row{
		Cells: []components.Cell{
			{Label: apiary.Name},
			{Label: apiary.Location},
			{Label: apiary.HoneyKind},
			{Label: strconv.Itoa(apiary.HiveCount)},
			{
				GroupedCells: []components.Cell{
					{
						UpdateRow: components.UpdateRowStrategy{
							Swap: "outerHTML",
						},
						ModalForm: components.ModalForm{
							Title: "Editer le rucher",
							ShowModalButton: components.Button{
								Icon: "edit",
							},
							SubmitFormButton: components.Button{
								Label:  "Sauvegarder",
								Type:   "is-link",
								FormId: fmt.Sprintf("apiary-edit-%s", apiary.Name),
							},
							Form: components.Form{
								Id:     fmt.Sprintf("apiary-edit-%s", apiary.Name),
								Method: "put",
								Url:    fmt.Sprintf("/apiary/%s", apiary.PublicId),
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
					{
						UpdateRow: components.UpdateRowStrategy{Swap: "delete"},
						Button: components.Button{
							Icon:    "delete",
							Confirm: "Supprimer le rucher ?",
							Url:     fmt.Sprintf("/apiary/%s", apiary.PublicId),
							Method:  "delete",
						},
					},
				},
			},
		},
	}

}

func GetApiaryBody(ctx context.Context, userId *uuid.UUID) (*bytes.Buffer, error) {
	apiaries, err := repositories.GetApiaries(ctx, userId)
	if err != nil {
		log.Printf("Could not get apiaries: %s", err)
		return nil, err
	}

	rows := []components.Row{}
	for _, apiary := range apiaries {
		rows = append(rows, GetApiaryTableRow(&apiary))
	}

	var locations []components.Choice
	for _, location := range repositories.GetApiaryValues(ctx, "location", userId) {
		locations = append(locations, components.Choice{Key: location, Label: location})
	}

	var honeyKinds []components.Choice
	for _, honeyKind := range repositories.GetApiaryValues(ctx, "honey_kind", userId) {
		honeyKinds = append(honeyKinds, components.Choice{Key: honeyKind, Label: honeyKind})
	}

	params := apiaryPageParameter{
		CreateApiaryModal: components.ModalForm{
			Title: "Création un nouveau rucher",
			ShowModalButton: components.Button{
				Label: "Nouveau rucher",
			},
			SubmitFormButton: components.Button{
				Label:  "Créer",
				FormId: "createApiary",
				Type:   "is-link",
			},
			Form: components.Form{
				Id:     "createApiary",
				Method: "post",
				Url:    "/apiary",
				Inputs: []components.Input{
					{
						Name:     "name",
						Label:    "Nom",
						Type:     "text",
						Required: true,
					},
					{
						Name:        "location",
						Label:       "Location",
						Type:        "text",
						Required:    true,
						ChoicesFree: locations,
					},
					{
						Name:        "honeyKind",
						Label:       "Type de miel",
						Type:        "text",
						Required:    true,
						ChoicesFree: honeyKinds,
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
