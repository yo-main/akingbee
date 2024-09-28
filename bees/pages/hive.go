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

func GetHiveTableRow(hive *models.Hive) components.Row {
	var apiaryName string
	if hive.Apiary != nil {
		apiaryName = hive.Apiary.Name
	}
	return components.Row{
		Cells: []components.Cell{
			{Label: hive.Name},
			{Label: hive.Condition},
			{Label: apiaryName},
			{
				GroupedCells: []components.Cell{
					{
						UpdateRow: components.UpdateRowStrategy{
							Swap: "outerHTML",
						},
						ModalForm: components.ModalForm{
							Title: "Editer la ruche",
							ShowModalButton: components.Button{
								Icon: "edit",
							},
							SubmitFormButton: components.Button{
								Label:  "Sauvegarder",
								Type:   "is-link",
								FormId: fmt.Sprintf("hive-edit-%s", hive.Name),
							},
							Form: components.Form{
								Id:     fmt.Sprintf("hive-edit-%s", hive.Name),
								Method: "put",
								Url:    fmt.Sprintf("/hive/%s", hive.PublicId),
								Swap:   "none",
								Inputs: []components.Input{
									{
										Name:     "name",
										Label:    "Nom",
										Type:     "text",
										Required: true,
										Default:  hive.Name,
									},
									{
										Name:     "condition",
										Label:    "État",
										Type:     "text",
										Required: true,
										Default:  hive.Condition,
									},
								},
							},
						},
					},
					{
						UpdateRow: components.UpdateRowStrategy{Swap: "delete"},
						Button: components.Button{
							Icon:    "delete",
							Confirm: "Supprimer la ruche ?",
							Url:     fmt.Sprintf("/hive/%s", hive.PublicId),
							Method:  "delete",
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

	conditions := repositories.GetHiveValues(ctx, "condition", userId)

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
				Swap:   "none",
				Inputs: []components.Input{
					{
						Name:     "name",
						Label:    "Nom",
						Type:     "text",
						Required: true,
					},
					{
						Name:     "condition",
						Label:    "Condition",
						Type:     "text",
						Required: true,
						Choices:  conditions,
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
				{Label: "Condition"},
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
