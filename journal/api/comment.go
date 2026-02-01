package api

import (
	"log"
	"net/http"
	"time"

	"github.com/google/uuid"

	"akingbee/bees/pages"
	api_helpers "akingbee/internal/web"
	overview_pages "akingbee/journal/pages"
	"akingbee/journal/repositories"
	comment_services "akingbee/journal/services/comment"
	user_models "akingbee/user/models"
	"akingbee/web"
)

func HandlePostCommentHive(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()
	_, ok := ctx.Value("authenticatedUser").(*user_models.AuthenticatedUser)

	if !ok {
		panic("unreacheable")
	}

	var err error
	var hivePublicID *uuid.UUID
	publicID, err := uuid.Parse(req.PathValue("hivePublicId"))
	if err != nil {
		log.Printf("Incorrect UUID: %s", err)
		web.PrepareFailedNotification(response, "Incorrect hive id: "+req.FormValue("hive_id"))
		response.WriteHeader(http.StatusNotFound)
		return
	}
	hivePublicID = &publicID

	var apiaryPublicID *uuid.UUID
	if value := req.FormValue("apiary_id"); value != "" {
		publicID, err := uuid.Parse(req.FormValue("apiary_id"))
		if err != nil {
			log.Printf("Incorrect UUID: %s", err)
			web.PrepareFailedNotification(response, "Incorrect apiary id: "+req.FormValue("apiary_id"))
			response.WriteHeader(http.StatusBadRequest)
			return
		}
		apiaryPublicID = &publicID
	}

	commentDate, err := time.Parse("2006-01-02", req.FormValue("date"))
	if err != nil {
		log.Printf("Date is not correctly formatted: %s", err)
		web.PrepareFailedNotification(response, "Date not correctly formatted: "+req.FormValue("date"))
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	command := comment_services.CreateCommentCommand{
		Date:           commentDate,
		Type:           req.FormValue("type"),
		Body:           req.FormValue("body"),
		HivePublicID:   hivePublicID,
		ApiaryPublicID: apiaryPublicID,
	}

	comment, err := comment_services.CreateComment(ctx, &command)
	if err != nil {
		log.Printf("Could not create comment: %s", err)
		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	commentRow, err := pages.GetCommentRow(comment).Build()
	if err != nil {
		log.Printf("Could not get comment row: %s", err)
		http.Redirect(response, req, "/", http.StatusBadRequest)
		return
	}

	web.PrepareSuccessNotification(response, "Comment created successfully")
	response.WriteHeader(http.StatusOK)
	api_helpers.WriteToResponse(response, commentRow.Bytes())
}

func HandlePutCommentHive(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()
	_, ok := ctx.Value("authenticatedUser").(*user_models.AuthenticatedUser)

	if !ok {
		panic("unreacheable")
	}

	commentPublicID, err := uuid.Parse(req.PathValue("commentPublicId"))
	if err != nil {
		log.Printf("The provided comment id is incorrect: %s", err)
		web.PrepareFailedNotification(response, "Not Found")
		response.WriteHeader(http.StatusNotFound)
		return
	}

	comment, err := repositories.GetComment(ctx, &commentPublicID)
	if err != nil {
		log.Printf("Comment not found: %s", err)
		web.PrepareFailedNotification(response, "Comment not found")
		response.WriteHeader(http.StatusNotFound)
		return
	}

	commentDate, err := time.Parse("2006-01-02", req.FormValue("date"))
	if err != nil {
		log.Printf("Date is not correctly formatted: %s", err)
	}

	comment.Date = commentDate
	comment.Type = req.FormValue("type")
	comment.Body = req.FormValue("body")

	err = comment_services.UpdateComment(ctx, comment)
	if err != nil {
		log.Printf("Could not update comment: %s", err)
		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	tableRow, err := pages.GetCommentRow(comment).Build()
	if err != nil {
		log.Printf("Could not get table row: %s", err)
		http.Redirect(response, req, "/", http.StatusBadRequest)
		return
	}

	web.PrepareSuccessNotification(response, "Comment updated successfully")
	response.WriteHeader(http.StatusOK)
	api_helpers.WriteToResponse(response, tableRow.Bytes())
}

func HandleDeleteComment(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()
	_, ok := ctx.Value("authenticatedUser").(*user_models.AuthenticatedUser)

	if !ok {
		panic("unreacheable")
	}

	commentPublicID, err := uuid.Parse(req.PathValue("commentPublicId"))
	if err != nil {
		log.Printf("The provided comment id is incorrect: %s", err)
		web.PrepareFailedNotification(response, "Bad request")
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	comment, err := repositories.GetComment(ctx, &commentPublicID)
	if err != nil {
		log.Printf("Comment not found: %s", err)
		web.PrepareFailedNotification(response, "Comment not found")
		response.WriteHeader(http.StatusNotFound)
		return
	}

	err = comment_services.DeleteComment(ctx, comment)
	if err != nil {
		log.Printf("Could not delete comment: %s", err)
		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	web.PrepareSuccessNotification(response, "Comment deleted successfully")
	response.WriteHeader(http.StatusOK)
}

func HandlePostCommentApiary(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()
	user, ok := ctx.Value("authenticatedUser").(*user_models.AuthenticatedUser)
	if !ok {
		panic("unreacheable")
	}

	// Parse apiary_id from form
	apiaryPublicID, err := uuid.Parse(req.FormValue("apiary_id"))
	if err != nil {
		log.Printf("Incorrect UUID: %s", err)
		web.PrepareFailedNotification(response, "Incorrect apiary id: "+req.FormValue("apiary_id"))
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	// Parse date
	commentDate, err := time.Parse("2006-01-02", req.FormValue("date"))
	if err != nil {
		log.Printf("Date is not correctly formatted: %s", err)
		web.PrepareFailedNotification(response, "Date not correctly formatted: "+req.FormValue("date"))
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	// Create command
	command := comment_services.CreateCommentCommand{
		Date:           commentDate,
		Type:           req.FormValue("type"),
		Body:           req.FormValue("body"),
		HivePublicID:   nil,
		ApiaryPublicID: &apiaryPublicID,
	}

	// Create comment
	_, err = comment_services.CreateComment(ctx, &command)
	if err != nil {
		log.Printf("Could not create comment: %s", err)
		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	// Get the entire card with updated comment
	card, err := overview_pages.GetApiaryCard(ctx, apiaryPublicID, &user.PublicID)
	if err != nil {
		log.Printf("Could not get apiary card: %s", err)
		web.PrepareFailedNotification(response, "Could not refresh card")
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	web.PrepareSuccessNotification(response, "Comment created successfully")
	response.WriteHeader(http.StatusOK)
	api_helpers.WriteToResponse(response, card.Bytes())
}

func HandlePutCommentApiary(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()
	user, ok := ctx.Value("authenticatedUser").(*user_models.AuthenticatedUser)
	if !ok {
		panic("unreacheable")
	}

	// Parse comment ID
	commentPublicID, err := uuid.Parse(req.PathValue("commentPublicId"))
	if err != nil {
		log.Printf("The provided comment id is incorrect: %s", err)
		web.PrepareFailedNotification(response, "Not Found")
		response.WriteHeader(http.StatusNotFound)
		return
	}

	// Get existing comment
	comment, err := repositories.GetComment(ctx, &commentPublicID)
	if err != nil {
		log.Printf("Comment not found: %s", err)
		web.PrepareFailedNotification(response, "Comment not found")
		response.WriteHeader(http.StatusNotFound)
		return
	}

	// Parse and validate date
	commentDate, err := time.Parse("2006-01-02", req.FormValue("date"))
	if err != nil {
		log.Printf("Date is not correctly formatted: %s", err)
		web.PrepareFailedNotification(response, "Date not correctly formatted")
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	// Update comment fields
	comment.Date = commentDate
	comment.Type = req.FormValue("type")
	comment.Body = req.FormValue("body")

	// Save update
	err = comment_services.UpdateComment(ctx, comment)
	if err != nil {
		log.Printf("Could not update comment: %s", err)
		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	// Need to get apiary ID from the comment
	if comment.ApiaryPublicID == nil {
		log.Printf("Comment is not associated with an apiary")
		web.PrepareFailedNotification(response, "Invalid comment")
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	// Get the entire card with updated comment
	card, err := overview_pages.GetApiaryCard(ctx, *comment.ApiaryPublicID, &user.PublicID)
	if err != nil {
		log.Printf("Could not get apiary card: %s", err)
		web.PrepareFailedNotification(response, "Could not refresh card")
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	web.PrepareSuccessNotification(response, "Comment updated successfully")
	response.WriteHeader(http.StatusOK)
	api_helpers.WriteToResponse(response, card.Bytes())
}
