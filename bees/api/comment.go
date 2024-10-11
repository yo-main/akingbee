package api

import (
	"akingbee/bees/pages"
	"akingbee/bees/repositories"
	comment_services "akingbee/bees/services/comment"
	user_services "akingbee/user/services"
	"akingbee/web"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/google/uuid"
)

func HandlePostComment(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()

	_, err := user_services.AuthenticateUser(req)

	if err != nil {
		log.Printf("Could not authenticate user: %s", err)
		web.PrepareFailedNotification(response, "Not authenticated")
		response.WriteHeader(http.StatusUnauthorized)
		return
	}

	hivePublicId, err := uuid.Parse(req.FormValue("hive_id"))
	if err != nil {
		log.Printf("Wrong hive id: %s", req.FormValue("hive_id"))
		web.PrepareFailedNotification(response, fmt.Sprintf("Invalid hive id: %s", req.FormValue("hive_id")))
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	commentDate, err := time.Parse("2006-01-02", req.FormValue("date"))
	if err != nil {
		log.Printf("Date is not correctly formatted: %s", err)
		web.PrepareFailedNotification(response, fmt.Sprintf("Date not correctly formatted: %s", req.FormValue("date")))
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	command := comment_services.CreateCommentCommand{
		Date:         commentDate,
		Type:         req.FormValue("type"),
		Body:         req.FormValue("body"),
		HivePublicId: hivePublicId,
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
	response.Write(commentRow.Bytes())
}

func HandlePutComment(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()

	_, err := user_services.AuthenticateUser(req)

	if err != nil {
		log.Printf("Could not authenticate user: %s", err)
		web.PrepareFailedNotification(response, "Not authenticated")
		response.WriteHeader(http.StatusUnauthorized)
		return
	}

	commentPublicId, err := uuid.Parse(req.PathValue("commentPublicId"))
	if err != nil {
		log.Printf("The provided comment id is incorrect: %s", err)
		web.PrepareFailedNotification(response, "Not Found")
		response.WriteHeader(http.StatusNotFound)
		return
	}

	comment, err := repositories.GetComment(ctx, &commentPublicId)
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
	response.Write(tableRow.Bytes())
}

func HandleDeleteComment(response http.ResponseWriter, req *http.Request) {
	ctx := req.Context()

	_, err := user_services.AuthenticateUser(req)

	if err != nil {
		log.Printf("Could not authenticate user: %s", err)
		web.PrepareFailedNotification(response, "Not authenticated")
		response.WriteHeader(http.StatusUnauthorized)
		return
	}

	commentPublicId, err := uuid.Parse(req.PathValue("commentPublicId"))
	if err != nil {
		log.Printf("The provided comment id is incorrect: %s", err)
		web.PrepareFailedNotification(response, "Bad request")
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	comment, err := repositories.GetComment(ctx, &commentPublicId)
	if err != nil {
		log.Printf("Hive not found: %s", err)
		web.PrepareFailedNotification(response, "Hive not found")
		response.WriteHeader(http.StatusNotFound)
		return
	}

	err = comment_services.DeleteComment(ctx, comment)
	if err != nil {
		log.Printf("Could not delete hive: %s", err)
		web.PrepareFailedNotification(response, err.Error())
		response.WriteHeader(http.StatusBadRequest)
		return
	}

	web.PrepareSuccessNotification(response, "Hive deleted successfully")
	response.WriteHeader(http.StatusOK)
}
