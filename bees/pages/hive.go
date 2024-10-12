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
)

var hivePageTemplate = template.Must(pages.HtmlPage.ParseFiles("bees/pages/templates/hive.html"))

type hivePageParameter struct {
	CreateHiveModal components.ModalForm
	Table           components.Table
}

func EditHiveModal(hive *models.Hive, showModalButton components.Button) *components.ModalForm {
	modal := components.ModalForm{
		Title:           "Editer la ruche",
		ShowModalButton: showModalButton,
		SubmitFormButton: components.Button{
			Label:  "Sauvegarder",
			Type:   "is-link",
			FormId: fmt.Sprintf("hive-edit-%s", hive.Name),
		},
		Form: components.Form{
			Id:     fmt.Sprintf("hive-edit-%s", hive.Name),
			Method: "put",
			Url:    fmt.Sprintf("/hive/%s", hive.PublicId),
			Inputs: []components.Input{
				{
					Name:     "name",
					Label:    "Nom",
					Type:     "text",
					Required: true,
					Default:  hive.Name,
				},
				{
					Name:     "beekeeper",
					Label:    "État",
					Type:     "text",
					Required: true,
					Default:  hive.Beekeeper,
				},
			},
		},
	}

	return &modal
}

func GetHiveTableRow(hive *models.Hive) components.Row {
	var apiaryName string
	if hive.Apiary != nil {
		apiaryName = hive.Apiary.Name
	}

	var swarmHealth string
	if hive.Swarm != nil {
		swarmHealth = hive.Swarm.Health
	}
	return components.Row{
		Cells: []components.Cell{
			{Label: hive.Name},
			{Label: hive.Beekeeper},
			{Label: swarmHealth},
			{Label: apiaryName},
			{
				GroupedCells: []components.Cell{
					{
						UpdateStrategy: &components.UpdateStrategy{
							Target:  "#page-body",
							Swap:    "innerHTML",
							Url:     fmt.Sprintf("/hive/%s", hive.PublicId),
							PushUrl: true,
							Method:  "get",
							Button: &components.Button{
								Icon: "eye",
							},
						},
					},
					{
						UpdateStrategy: &components.UpdateStrategy{
							Target: "closest tr",
							Swap:   "outerHTML",
							Modal: EditHiveModal(
								hive,
								components.Button{
									Icon: "edit",
								},
							),
						},
					},
					{
						UpdateStrategy: &components.UpdateStrategy{
							Target:  "closest tr",
							Swap:    "delete",
							Url:     fmt.Sprintf("/hive/%s", hive.PublicId),
							Method:  "delete",
							Confirm: "Supprimer la ruche ?",
							Button: &components.Button{
								Icon: "delete",
							},
						},
					},
				},
			},
		},
	}

}

func GetHivesBody(ctx context.Context, userId *uuid.UUID) (*bytes.Buffer, error) {
	hives, err := repositories.GetHives(ctx, userId)
	if err != nil {
		log.Printf("Could not get hives: %s", err)
		return nil, err
	}

	rows := []components.Row{}
	for _, hive := range hives {
		rows = append(rows, GetHiveTableRow(hive))
	}

	var beekeepers []components.Choice
	for _, beekeeper := range repositories.GetHiveValues(ctx, "beekeeper", userId) {
		beekeepers = append(beekeepers, components.Choice{Key: beekeeper, Label: beekeeper})
	}

	apiaries, err := repositories.GetApiaries(ctx, userId)
	if err != nil {
		log.Printf("Could not load apiaries: %s", err)
		return nil, err
	}

	var apiaryChoices = []components.Choice{
		{Key: "none", Label: "Aucun", Selected: true, Disabled: true},
	}

	var swarmHealths []components.Choice
	for _, swarmHealth := range repositories.GetSwarmValues(ctx, "health", userId) {
		swarmHealths = append(swarmHealths, components.Choice{Key: swarmHealth, Label: swarmHealth})
	}

	for _, apiary := range apiaries {
		apiaryChoices = append(apiaryChoices, components.Choice{Key: apiary.PublicId.String(), Label: apiary.Name})
	}

	params := hivePageParameter{
		CreateHiveModal: components.ModalForm{
			Title: "Création d'une nouvelle ruche",
			ShowModalButton: components.Button{
				Label: "Nouvelle ruche",
			},
			SubmitFormButton: components.Button{
				Label:  "Créer",
				FormId: "createHive",
				Type:   "is-link",
			},
			Form: components.Form{
				Id:     "createHive",
				Method: "post",
				Url:    "/hive",
				Inputs: []components.Input{
					{
						Name:     "name",
						Label:    "Nom",
						Type:     "text",
						Required: true,
					},
					{
						Name:        "beekeeper",
						Label:       "Apiculteur",
						Type:        "text",
						Required:    true,
						ChoicesFree: beekeepers,
					},
					{
						Name:        "swarm_health",
						Label:       "Santé de l'essaim",
						Type:        "text",
						Required:    true,
						ChoicesFree: swarmHealths,
					},
					{
						Name:          "apiary",
						Label:         "Rucher",
						Type:          "text",
						Required:      true,
						ChoicesStrict: apiaryChoices,
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
				{Label: "Apiculteur"},
				{Label: "Santé de l'essaim"},
				{Label: "Rucher"},
				{Label: "Actions"},
			},
			Rows: rows,
		}}

	var hivePage bytes.Buffer
	err = pages.HtmlPage.ExecuteTemplate(&hivePage, "hive.html", params)

	if err != nil {
		log.Printf("Failed to build hive page: %s", err)
		return nil, err
	}

	return &hivePage, nil

}

func HandleGetHive(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()

	userId, err := services.AuthenticateUser(req)

	if err != nil {
		log.Printf("Could not authenticate user: %s", err)
		response.WriteHeader(http.StatusUnauthorized)
		return
	}

	hivePage, err := GetHivesBody(ctx, userId)
	if err != nil {
		log.Printf("Could not get hive page: %s", err)
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	if htmx.IsHtmxRequest(req) {
		response.Write(hivePage.Bytes())
	} else {
		web.ReturnFullPage(ctx, response, *hivePage, userId)
	}
}
