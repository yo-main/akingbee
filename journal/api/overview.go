package api

import (
	"log"
	"net/http"

	api_helpers "akingbee/internal/web"
	overview_api "akingbee/journal/pages"
	user_models "akingbee/user/models"
)

func HandleGetOverview(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()

	user, ok := ctx.Value("authenticatedUser").(*user_models.AuthenticatedUser)
	if !ok {
		panic("unreacheable")
	}

	overviewPage, err := overview_api.GetOverviewBody(ctx, &user.PublicID)
	if err != nil {
		log.Printf("Could not get overview page: %s", err)
		response.WriteHeader(http.StatusBadRequest)

		return
	}

	api_helpers.WriteToResponse(response, overviewPage.Bytes())
}
