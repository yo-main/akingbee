package pages

import (
	"akingbee/bees/models"
	"akingbee/bees/repositories"

	user_models "akingbee/user/models"
	"akingbee/web/components"
	"akingbee/web/pages"
	"bytes"
	"context"
	"embed"
	"fmt"
	"github.com/google/uuid"
	"html/template"
	"log"
	"net/http"
	"strconv"
)

//go:embed templates/*
var TemplatesFS embed.FS

var apiaryPageTemplate = template.Must(pages.HtmlPage.ParseFS(TemplatesFS, "templates/apiary.html"))

type apiaryPageParameter struct {
	CreateApiaryModal components.UpdateStrategy
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
						UpdateStrategy: &components.UpdateStrategy{
							Swap:   "outerHTML",
							Target: "closest tr",
							Modal: &components.ModalForm{
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
					},
					{
						UpdateStrategy: &components.UpdateStrategy{
							Swap:    "delete",
							Target:  "closest tr",
							Confirm: "Supprimer le rucher ?",
							Button: &components.Button{
								Icon:   "delete",
								Url:    fmt.Sprintf("/apiary/%s", apiary.PublicId),
								Method: "delete",
							},
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
		CreateApiaryModal: components.UpdateStrategy{
			Target: "#page-body",
			Swap:   "innerHTML",
			Modal: &components.ModalForm{
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

	if user, ok := ctx.Value("authenticatedUser").(*user_models.User); ok {
		apiaryPage, err := GetApiaryBody(ctx, &user.PublicId)
		if err != nil {
			log.Printf("Could not get apiry page: %s", err)
			response.WriteHeader(http.StatusBadRequest)
			return
		}

		response.Write(apiaryPage.Bytes())
	} else {
		panic("unreacheable")
	}

}
