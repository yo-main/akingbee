package pages

import (
	"bytes"
	"context"
	"embed"
	"fmt"
	"html/template"
	"log"
	"net/http"
	"strconv"

	"github.com/google/uuid"

	"akingbee/bees/models"
	"akingbee/bees/repositories"
	api_helpers "akingbee/internal/web"
	user_models "akingbee/user/models"
	"akingbee/web/components"
	"akingbee/web/pages"
)

//go:embed templates/*
var TemplatesFS embed.FS

var _ = template.Must(pages.HtmlPage.ParseFS(TemplatesFS, "templates/apiary.html"))

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
									FormID: "apiary-edit-" + apiary.Name,
								},
								Form: components.Form{
									ID:     "apiary-edit-" + apiary.Name,
									Method: "put",
									URL:    fmt.Sprintf("/apiary/%s", apiary.PublicID),
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
								URL:    fmt.Sprintf("/apiary/%s", apiary.PublicID),
								Method: "delete",
							},
						},
					},
				},
			},
		},
	}
}

func GetApiaryBody(ctx context.Context, userID *uuid.UUID) (*bytes.Buffer, error) {
	apiaries, err := repositories.GetApiaries(ctx, userID)
	if err != nil {
		log.Printf("Could not get apiaries: %s", err)

		return nil, fmt.Errorf("could not get apiaries: %w", err)
	}

	rows := []components.Row{}
	for _, apiary := range apiaries {
		rows = append(rows, GetApiaryTableRow(&apiary))
	}

	locations := repositories.GetApiaryValues(ctx, "location", userID)
	locationChoices := make([]components.Choice, len(locations))

	for i, location := range locations {
		locationChoices[i] = components.Choice{Key: location, Label: location}
	}

	honeyKinds := repositories.GetApiaryValues(ctx, "honey_kind", userID)
	honeyKindChoices := make([]components.Choice, len(honeyKinds))

	for i, honeyKind := range honeyKinds {
		honeyKindChoices[i] = components.Choice{Key: honeyKind, Label: honeyKind}
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
					FormID: "createApiary",
					Type:   "is-link",
				},
				Form: components.Form{
					ID:     "createApiary",
					Method: "post",
					URL:    "/apiary",
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
							ChoicesFree: locationChoices,
						},
						{
							Name:        "honeyKind",
							Label:       "Type de miel",
							Type:        "text",
							Required:    true,
							ChoicesFree: honeyKindChoices,
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

		return nil, fmt.Errorf("failed to build apiary: %w", err)
	}

	return &apiaryPage, nil
}

func HandleGetApiary(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()

	if user, ok := ctx.Value("authenticatedUser").(*user_models.User); ok {
		apiaryPage, err := GetApiaryBody(ctx, &user.PublicID)
		if err != nil {
			log.Printf("Could not get apiry page: %s", err)
			response.WriteHeader(http.StatusBadRequest)

			return
		}

		api_helpers.WriteToResponse(response, apiaryPage.Bytes())
	} else {
		panic("unreacheable")
	}

}
