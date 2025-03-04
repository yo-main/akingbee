package api

import (
	"bytes"
	"fmt"
	"html/template"
	"log"
	"net/http"
	"strconv"
	"time"

	"github.com/google/uuid"

	"akingbee/bees/models"
	hive_pages "akingbee/bees/pages"
	"akingbee/bees/repositories"
	services "akingbee/bees/services/harvest"
	user_models "akingbee/user/models"
	"akingbee/web"
	"akingbee/web/components"
	"akingbee/web/pages"
)

var HarvestDetailTemplate = template.Must(pages.HtmlPage.ParseFS(hive_pages.TemplatesFS, "templates/hive_detail_harvest.html"))

type HiveHarvestDetail struct {
	CreateHarvestForm components.UpdateStrategy
	HarvestsTable     components.Table
}

func HandlePostHarvest(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()

	user, ok := ctx.Value("authenticatedUser").(*user_models.User)
	if ok == false {
		panic("unreacheable")
	}

	hivePublicID, err := uuid.Parse(req.PathValue("hivePublicId"))
	if err != nil {
		log.Printf("The provided hive id is incorrect: %s", err)
		web.PrepareFailedNotification(response, "Not Found")
		response.WriteHeader(http.StatusNotFound)
		return
	}

	hive, err := repositories.GetHive(ctx, &hivePublicID)
	if err != nil {
		web.PrepareFailedNotification(response, "Not Found")
		response.WriteHeader(http.StatusNotFound)
		return
	}
	if hive.User != user.PublicID {
		web.PrepareFailedNotification(response, "Forbidden")
		response.WriteHeader(http.StatusForbidden)
		return
	}

	quantity, err := strconv.Atoi(req.FormValue("quantity"))
	if err != nil {
		log.Printf("The provided quantity is incorrect: %s", err)
		web.PrepareFailedNotification(response, "Incorrect quantity")
		response.WriteHeader(http.StatusBadRequest)
		return
	}
	date, err := time.Parse("2006-01-02", req.FormValue("date"))
	if err != nil {
		log.Printf("The provided date is incorrect: %s", err)
		web.PrepareFailedNotification(response, "Incorrect date")
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	command := services.CreateHarvestCommand{
		Date:         date,
		Quantity:     quantity,
		HivePublicID: &hivePublicID,
	}

	harvest, err := services.CreateHarvest(ctx, &command)
	if err != nil {
		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	row, err := GetHarvestRow(harvest).Build()
	if err != nil {
		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	web.PrepareSuccessNotification(response, "Harvest created successfully")
	response.Write(row.Bytes())
	response.WriteHeader(http.StatusOK)
}

func HandleGetHiveHarvests(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()

	user, ok := ctx.Value("authenticatedUser").(*user_models.User)
	if ok == false {
		panic("unreacheable")
	}

	hivePublicID, err := uuid.Parse(req.PathValue("hivePublicId"))
	if err != nil {
		log.Printf("The provided hive id is incorrect: %s", err)
		web.PrepareFailedNotification(response, "Not Found")
		response.WriteHeader(http.StatusNotFound)
		return
	}

	hive, err := repositories.GetHive(ctx, &hivePublicID)
	if err != nil {
		web.PrepareFailedNotification(response, "Not Found")
		response.WriteHeader(http.StatusNotFound)
		return
	}

	if hive.User != user.PublicID {
		web.PrepareFailedNotification(response, "Forbidden")
		response.WriteHeader(http.StatusForbidden)
		return
	}

	harvests, err := repositories.GetHarvests(ctx, &hivePublicID)
	if err != nil {
		web.PrepareFailedNotification(response, "Could not get harvests")
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	params := GetHarvestsDetail(hive, harvests)

	var content bytes.Buffer
	err = pages.HtmlPage.ExecuteTemplate(&content, "hive_detail_harvest.html", &params)

	if err != nil {
		web.PrepareFailedNotification(response, "Could not build harvest table")
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	response.Write(content.Bytes())
}

func GetHarvestsDetail(hive *models.Hive, harvests []models.Harvest) *HiveHarvestDetail {
	var harvestRows []components.Row
	for _, harvest := range harvests {
		harvestRows = append(harvestRows, *GetHarvestRow(&harvest))
	}

	return &HiveHarvestDetail{
		CreateHarvestForm: components.UpdateStrategy{
			Target: "#table-hive-harvests",
			Swap:   "afterbegin",
			Modal: &components.ModalForm{
				Title: "Nouvelle récolte",
				ShowModalButton: components.Button{
					Label: "Nouvelle récolte",
				},
				SubmitFormButton: components.Button{
					Label:  "Créer",
					FormID: "create-harvest",
					Type:   "is-link",
				},
				Form: components.Form{
					ID:     "create-harvest",
					Method: "post",
					URL:    fmt.Sprintf("/hive/%s/harvests", hive.PublicID),
					Inputs: []components.Input{
						{
							Name:        "quantity",
							Label:       "Quantité",
							Required:    true,
							Type:        "number",
							Placeholder: "en gramme",
						},
						{
							Name:     "date",
							Label:    "Date de la récolte",
							Required: true,
							Type:     "date",
							Default:  time.Now().Format("2006-01-02"),
						},
					},
				},
			},
		},
		HarvestsTable: components.Table{
			ID:          "table-hive-harvests",
			IsFullWidth: true,
			IsStripped:  true,
			Headers: []components.Header{
				{Label: "Actions"},
				{Label: "Date"},
				{Label: "Quantity"},
			},
			ColumnSizes: []components.ColumnSize{
				{Span: "1", Style: "width: 10%"},
				{Span: "1", Style: "width: 30%"},
				{Span: "1", Style: "width: 60%"},
			},
			Rows: harvestRows,
		},
	}
}

func GetHarvestRow(harvest *models.Harvest) *components.Row {
	params := components.Row{
		Cells: []components.Cell{
			{
				GroupedCells: []components.Cell{
					{
						UpdateStrategy: &components.UpdateStrategy{
							Swap:    "delete",
							Target:  "closest tr",
							Confirm: "Supprimer la recolte ?",
							Button: &components.Button{
								Icon:   "delete",
								URL:    fmt.Sprintf("/hive/%s/harvests/%s", harvest.HivePublicID, harvest.PublicID),
								Method: "delete",
							},
						},
					},
				},
			},
			{Label: harvest.Date.Format("2006-01-02")},
			{Label: fmt.Sprintf("%d", harvest.Quantity)},
		},
	}

	return &params
}

func HandleDeleteHarvest(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()
	_, ok := ctx.Value("authenticatedUser").(*user_models.User)
	if ok == false {
		panic("unreacheable")
	}

	harvestPublicID, err := uuid.Parse(req.PathValue("harvestPublicId"))
	if err != nil {
		log.Printf("The provided harvest id is incorrect: %s", err)
		web.PrepareFailedNotification(response, "Bad request")
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	harvest, err := repositories.GetHarvest(ctx, &harvestPublicID)
	if err != nil {
		log.Printf("Harvest not found: %s", err)
		web.PrepareFailedNotification(response, "Harvest not found")
		response.WriteHeader(http.StatusNotFound)
		return
	}

	err = repositories.DeleteHarvest(ctx, harvest)
	if err != nil {
		log.Printf("Could not delete harvest: %s", err)
		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	web.PrepareSuccessNotification(response, "Harvest deleted successfully")
	response.WriteHeader(http.StatusOK)
}
