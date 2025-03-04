package pages

import (
	"bytes"
	"context"
	"fmt"
	"html/template"
	"log"
	"net/http"

	"github.com/google/uuid"

	"akingbee/bees/models"
	"akingbee/bees/repositories"
	api_helpers "akingbee/internal/web"
	user_models "akingbee/user/models"
	"akingbee/web/components"
	"akingbee/web/pages"
)

var _ = template.Must(pages.HtmlPage.ParseFS(TemplatesFS, "templates/hive.html"))

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
	elementType string,
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
				FormID: "hive-edit-" + hive.Name,
			},
			Form: components.Form{
				ID:     "hive-edit-" + hive.Name,
				Method: "put",
				URL:    "/hive/" + hive.PublicID.String(),
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
						Name:     "swarm_year",
						Label:    "Année de la reine",
						Type:     "integer",
						Required: true,
						Default:  hive.GetSwarmYear(),
					},
					{
						Name:          "apiary",
						Label:         "Rucher",
						Type:          "text",
						Required:      true,
						ChoicesStrict: apiaryChoices,
						Default:       hive.GetApiaryPublicID(),
					},
					{
						Name:     "elementType",
						Label:    "elementType",
						Type:     "text",
						Required: true,
						Default:  elementType,
						Hidden:   true,
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
								URL:     fmt.Sprintf("/hive/%s", hive.PublicID),
								Method:  "get",
								PushURL: true,
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
							"row",
						),
					},
					{
						UpdateStrategy: &components.UpdateStrategy{
							Target:  "closest tr",
							Swap:    "delete",
							Confirm: "Supprimer la ruche ?",
							Button: &components.Button{
								Icon:   "delete",
								URL:    fmt.Sprintf("/hive/%s", hive.PublicID),
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
			Key:      apiary.PublicID.String(),
			Label:    apiary.Name,
			Selected: selected,
		})
	}

	return apiaryChoices
}

func GetSwarmHealthChoices(swarmHealths []string, hive *models.Hive) []components.Choice {
	var swarmHealthChoices = make([]components.Choice, len(swarmHealths))

	for index, swarmHealth := range swarmHealths {
		var selected bool
		if hive != nil {
			selected = hive.GetSwarmHealth() == swarmHealth
		}

		swarmHealthChoices[index] = components.Choice{
			Key:      swarmHealth,
			Label:    swarmHealth,
			Selected: selected,
		}
	}

	return swarmHealthChoices
}

func GetBeekeeperChoices(beekeepers []string, hive *models.Hive) []components.Choice {
	var beekeeperChoices = make([]components.Choice, len(beekeepers))

	for index, beekeeper := range beekeepers {
		var selected bool
		if hive != nil {
			selected = hive.Beekeeper == beekeeper
		}

		beekeeperChoices[index] = components.Choice{
			Key:      beekeeper,
			Label:    beekeeper,
			Selected: selected,
		}
	}

	return beekeeperChoices
}

func GetHivesBody(ctx context.Context, userID *uuid.UUID) (*bytes.Buffer, error) {
	hives, err := repositories.GetHives(ctx, userID)
	if err != nil {
		log.Printf("Could not get hives: %s", err)
		return nil, err
	}

	apiaries, _ := repositories.GetApiaries(ctx, userID)
	swarmHealths := repositories.GetSwarmValues(ctx, "health", userID)
	beekeepers := repositories.GetHiveValues(ctx, "beekeeper", userID)

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
					FormID: "createHive",
					Type:   "is-link",
				},
				Form: components.Form{
					ID:     "createHive",
					Method: "post",
					URL:    "/hive",
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

	if user, ok := ctx.Value("authenticatedUser").(*user_models.User); ok {
		hivePage, err := GetHivesBody(ctx, &user.PublicID)
		if err != nil {
			log.Printf("Could not get hive page: %s", err)
			response.WriteHeader(http.StatusBadRequest)

			return
		}

		api_helpers.WriteToResponse(response, hivePage.Bytes())
	} else {
		panic("unreacheable")
	}
}
