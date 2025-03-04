package api

import (
	"log"
	"net/http"
	"time"

	"github.com/google/uuid"

	"akingbee/bees/pages"
	"akingbee/bees/repositories"
	comment_services "akingbee/bees/services/comment"
	api_helpers "akingbee/internal/web"
	user_models "akingbee/user/models"
	"akingbee/web"
)

func HandlePostComment(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()
	_, ok := ctx.Value("authenticatedUser").(*user_models.User)

	if !ok {
		panic("unreacheable")
	}

	hivePublicID, err := uuid.Parse(req.FormValue("hive_id"))
	if err != nil {
		log.Printf("Wrong hive id: %s", req.FormValue("hive_id"))
		web.PrepareFailedNotification(response, "Invalid hive id: "+req.FormValue("hive_id"))
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	commentDate, err := time.Parse("2006-01-02", req.FormValue("date"))
	if err != nil {
		log.Printf("Date is not correctly formatted: %s", err)
		web.PrepareFailedNotification(response, "Date not correctly formatted: "+req.FormValue("date"))
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	command := comment_services.CreateCommentCommand{
		Date:         commentDate,
		Type:         req.FormValue("type"),
		Body:         req.FormValue("body"),
		HivePublicID: hivePublicID,
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

func HandlePutComment(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()
	_, ok := ctx.Value("authenticatedUser").(*user_models.User)

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
	_, ok := ctx.Value("authenticatedUser").(*user_models.User)

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
