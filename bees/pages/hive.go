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
	CreateHiveModal components.UpdateStrategy
	Table           components.Table
}

func EditHiveModal(
	hive *models.Hive,
	apiaryChoices []components.Choice,
	swarmHealthChoices []components.Choice,
	beekeeperChoices []components.Choice,
	showModalButton components.Button,
	target string,
	swap string,
) *components.UpdateStrategy {
	return &components.UpdateStrategy{
		Target: target,
		Swap:   swap,
		Modal: &components.ModalForm{
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
						Name:        "beekeeper",
						Label:       "Apiculteur",
						Type:        "text",
						Required:    true,
						ChoicesFree: beekeeperChoices,
						Default:     hive.Beekeeper,
					},
					{
						Name:        "swarm_health",
						Label:       "Santé de l'essaim",
						Type:        "text",
						Required:    true,
						ChoicesFree: swarmHealthChoices,
						Default:     hive.GetSwarmHealth(),
					},
					{
						Name:          "apiary",
						Label:         "Rucher",
						Type:          "text",
						Required:      true,
						ChoicesStrict: apiaryChoices,
						Default:       hive.GetApiaryPublicId(),
					},
				},
			},
		},
	}
}

func GetHiveTableRow(
	hive *models.Hive,
	apiaryChoices []components.Choice,
	swarmHealthChoices []components.Choice,
	beekeeperChoices []components.Choice,
) components.Row {
	apiaryName := hive.GetApiaryName()
	swarmHealth := hive.GetSwarmHealth()

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
							Target: "#page-body",
							Swap:   "innerHTML",
							Button: &components.Button{
								Icon:    "eye",
								Url:     fmt.Sprintf("/hive/%s", hive.PublicId),
								Method:  "get",
								PushUrl: true,
							},
						},
					},
					{
						UpdateStrategy: EditHiveModal(
							hive,
							apiaryChoices,
							swarmHealthChoices,
							beekeeperChoices,
							components.Button{Icon: "edit"},
							"closest tr",
							"outerHTML",
						),
					},
					{
						UpdateStrategy: &components.UpdateStrategy{
							Target:  "closest tr",
							Swap:    "delete",
							Confirm: "Supprimer la ruche ?",
							Button: &components.Button{
								Icon:   "delete",
								Url:    fmt.Sprintf("/hive/%s", hive.PublicId),
								Method: "delete",
							},
						},
					},
				},
			},
		},
	}

}

func GetApiariesChoices(apiaries []models.Apiary, hive *models.Hive) []components.Choice {
	var apiaryChoices = []components.Choice{
		{Key: "none", Label: "Stock", Selected: true},
	}

	for _, apiary := range apiaries {
		var selected bool
		if hive != nil {
			selected = hive.GetApiaryName() == apiary.Name
		}

		apiaryChoices = append(apiaryChoices, components.Choice{
			Key:      apiary.PublicId.String(),
			Label:    apiary.Name,
			Selected: selected,
		})
	}

	return apiaryChoices
}

func GetSwarmHealthChoices(swarmHealths []string, hive *models.Hive) []components.Choice {
	var swarmHealthChoices []components.Choice

	for _, swarmHealth := range swarmHealths {
		var selected bool
		if hive != nil {
			selected = hive.GetSwarmHealth() == swarmHealth
		}

		swarmHealthChoices = append(swarmHealthChoices, components.Choice{
			Key:      swarmHealth,
			Label:    swarmHealth,
			Selected: selected,
		})
	}
	return swarmHealthChoices
}

func GetBeekeeperChoices(beekeepers []string, hive *models.Hive) []components.Choice {
	var beekeeperChoices []components.Choice

	for _, beekeeper := range beekeepers {
		var selected bool
		if hive != nil {
			selected = hive.Beekeeper == beekeeper
		}

		beekeeperChoices = append(beekeeperChoices, components.Choice{
			Key:      beekeeper,
			Label:    beekeeper,
			Selected: selected,
		})
	}

	return beekeeperChoices
}

func GetHivesBody(ctx context.Context, userId *uuid.UUID) (*bytes.Buffer, error) {
	hives, err := repositories.GetHives(ctx, userId)
	if err != nil {
		log.Printf("Could not get hives: %s", err)
		return nil, err
	}

	apiaries, _ := repositories.GetApiaries(ctx, userId)
	swarmHealths := repositories.GetSwarmValues(ctx, "health", userId)
	beekeepers := repositories.GetHiveValues(ctx, "beekeeper", userId)

	rows := []components.Row{}
	for _, hive := range hives {
		rows = append(
			rows,
			GetHiveTableRow(
				hive,
				GetApiariesChoices(apiaries, hive),
				GetSwarmHealthChoices(swarmHealths, hive),
				GetBeekeeperChoices(beekeepers, hive),
			),
		)
	}

	params := hivePageParameter{
		CreateHiveModal: components.UpdateStrategy{
			Target: "#page-body",
			Swap:   "innerHTML",
			Modal: &components.ModalForm{
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
							ChoicesFree: GetBeekeeperChoices(beekeepers, nil),
						},
						{
							Name:        "swarm_health",
							Label:       "Santé de l'essaim",
							Type:        "text",
							Required:    true,
							ChoicesFree: GetSwarmHealthChoices(swarmHealths, nil),
						},
						{
							Name:          "apiary",
							Label:         "Rucher",
							Type:          "text",
							Required:      true,
							ChoicesStrict: GetApiariesChoices(apiaries, nil),
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
