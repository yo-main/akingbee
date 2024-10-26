FROM golang:1.22-bookworm AS builder

WORKDIR /app

# Copy the Go module files and download dependencies
COPY go.mod go.sum ./
RUN go mod download

# Copy the rest of the application code
COPY . .

# Build the Go app statically
RUN CGO_ENABLED=1 GOOS=linux go build -o /app/akingbee .

# --- Stage 2: Runner ---
# Use a minimal base image to run the app
FROM golang:1.22-bookworm

# Copy the binary from the builder stage
COPY --from=builder /app/akingbee /akingbee

WORKDIR /app
COPY . .

EXPOSE 8080

# Command to run the Go app
ENTRYPOINT ["/akingbee"]

