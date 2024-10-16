package api

import (
	"akingbee/bees/models"
	"akingbee/bees/repositories"

	services "akingbee/bees/services/harvest"
	user_services "akingbee/user/services"
	"akingbee/web"
	"akingbee/web/components"
	"fmt"
	"log"
	"net/http"
	"strconv"
	"time"

	"github.com/google/uuid"
)

func HandlePostHarvest(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()

	userId, err := user_services.AuthenticateUser(req)

	if err != nil {
		log.Printf("Could not authenticate user: %s", err)
		web.PrepareFailedNotification(response, "Not authenticated")
		response.WriteHeader(http.StatusUnauthorized)
		return
	}

	hivePublicId, err := uuid.Parse(req.PathValue("hivePublicId"))
	if err != nil {
		log.Printf("The provided hive id is incorrect: %s", err)
		web.PrepareFailedNotification(response, "Not Found")
		response.WriteHeader(http.StatusNotFound)
		return
	}

	hive, err := repositories.GetHive(ctx, &hivePublicId)
	if err != nil {
		web.PrepareFailedNotification(response, "Not Found")
		response.WriteHeader(http.StatusNotFound)
		return
	}
	if hive.User != *userId {
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
		HivePublicId: &hivePublicId,
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

	userId, err := user_services.AuthenticateUser(req)

	if err != nil {
		log.Printf("Could not authenticate user: %s", err)
		web.PrepareFailedNotification(response, "Not authenticated")
		response.WriteHeader(http.StatusUnauthorized)
		return
	}

	hivePublicId, err := uuid.Parse(req.PathValue("hivePublicId"))
	if err != nil {
		log.Printf("The provided hive id is incorrect: %s", err)
		web.PrepareFailedNotification(response, "Not Found")
		response.WriteHeader(http.StatusNotFound)
		return
	}

	hive, err := repositories.GetHive(ctx, &hivePublicId)
	if err != nil {
		web.PrepareFailedNotification(response, "Not Found")
		response.WriteHeader(http.StatusNotFound)
		return
	}

	if hive.User != *userId {
		web.PrepareFailedNotification(response, "Forbidden")
		response.WriteHeader(http.StatusForbidden)
		return
	}

	harvests, err := repositories.GetHarvests(ctx, &hivePublicId)
	if err != nil {
		web.PrepareFailedNotification(response, "Could not get harvests")
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	table, err := GetHarvestsTable(harvests).Build()
	if err != nil {
		web.PrepareFailedNotification(response, "Could not build harvest table")
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	response.Write(table.Bytes())
}

func GetHarvestsTable(harvests []models.Harvest) *components.Table {
	var harvestRows []components.Row
	for _, harvest := range harvests {
		harvestRows = append(harvestRows, *GetHarvestRow(&harvest))
	}

	return &components.Table{
		Id:          "table-hive-harvests",
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
								Url:    fmt.Sprintf("/hive/%s/harvest/%s", harvest.HivePublicId, harvest.PublicId),
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
