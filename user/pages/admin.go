package pages

import (
	"bytes"
	"context"
	"fmt"
	"html/template"
	"log"
	"net/http"

	"akingbee/user/models"
	userRepository "akingbee/user/repositories"
	"akingbee/web/components"
	"akingbee/web/pages"
)

var adminPageTemplate = template.Must(pages.HtmlPage.ParseFS(templatesFS, "templates/admin.html"))

type AdminPageBuilder struct {
	UserTable components.Table
}

func HandleGetAdmin(response http.ResponseWriter, req *http.Request) {
	adminPage, err := getAdminPage(req.Context())
	if err != nil {
		log.Printf("Could not build admin page: %s", err)
		return
	}

	response.Write(adminPage.Bytes())
}

func getAdminPage(ctx context.Context) (*bytes.Buffer, error) {
	users, err := userRepository.ListUsers(ctx)
	if err != nil {
		return nil, err
	}

	var userRows []components.Row
	for _, user := range users {
		userRows = append(userRows, getUserRow(user))
	}

	params := AdminPageBuilder{
		UserTable: components.Table{
			ID:          "table-users",
			IsFullWidth: true,
			IsStripped:  true,
			Headers: []components.Header{
				{Label: "Username"},
				{Label: "Email"},
				{Label: "Actions"},
			},
			ColumnSizes: []components.ColumnSize{
				{Span: "1", Style: "width: 40%"},
				{Span: "1", Style: "width: 40%"},
				{Span: "1", Style: "width: 20%"},
			},
			Rows: userRows,
		},
	}

	var content bytes.Buffer
	err = pages.HtmlPage.ExecuteTemplate(&content, "admin.html", &params)

	if err != nil {
		return nil, err
	}

	return &content, nil
}

func getUserRow(user *models.User) components.Row {
	return components.Row{
		Cells: []components.Cell{
			{Label: user.Credentials.Username},
			{Label: user.Email},
			{
				GroupedCells: []components.Cell{
					{
						UpdateStrategy: &components.UpdateStrategy{
							Swap: "none",
							Button: &components.Button{
								Icon:   "ninja",
								URL:    fmt.Sprintf("/user/%s/impersonate", user.PublicID.String()),
								Method: "post",
							},
						},
					},
				},
			},
		},
	}
}
