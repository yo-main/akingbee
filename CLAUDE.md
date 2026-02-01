# CLAUDE.md

## Project Overview

Akingbee is a beekeeping management website built with Go backend and HTMX frontend, using SQLite for data persistence. The application helps beekeepers manage their hives, apiaries, harvests, and keep a journal of activities.

## Development Commands

### Running the application
```bash
go run .                    # Start server on localhost:8080
just api                    # Alternative using justfile
```

### Dependencies
```bash
go mod download            # Download all dependencies
```

### Code quality
```bash
go fmt                     # Format code
golangci-lint run          # Run linter (configured in .golangci.yaml)
```

### Testing
```bash
go test ./...              # Run all tests
go test ./auth/token       # Run tests in specific package
```

### Docker
```bash
docker build -t akingbee . # Build Docker image
```

## Architecture

### Domain Structure

The codebase follows a domain-driven design with three main domains:

- **bees/**: Core beekeeping functionality (apiaries, hives, harvests, swarms)
- **user/**: User management and authentication
- **journal/**: Activity tracking and comments

Each domain follows a consistent structure:
```
<domain>/
  ├── api/           # HTTP endpoint handlers
  ├── pages/         # HTMX page handlers and HTML templates
  ├── services/      # Business logic
  ├── repositories/  # Database access layer
  └── models/        # Domain data structures
```

### Routing and Middleware

All HTTP routing is centralized in `entrypoints/app.go`. The app uses three middleware layers defined in `internal/web/api.go`:

- **Authenticated**: Requires valid JWT token, rejects unauthorized requests
- **OptionallyAuthenticated**: Allows both authenticated and anonymous access
- **HtmxMiddleware**: Wraps responses in full page template for non-HTMX requests, returns fragments for HTMX requests

Route pattern:
```go
mux.HandleFunc("POST /hive/{hivePublicId}/comments",
    web.Authenticated(api_journal.HandlePostCommentHive))
```

### HTMX Integration

The frontend uses HTMX for dynamic interactions. The `HtmxMiddleware` in `internal/web/api.go` detects HTMX requests via headers:
- Non-HTMX requests receive full HTML pages wrapped in the layout template
- HTMX requests receive only HTML fragments for targeted swaps

Templates are stored in `<domain>/pages/templates/` and component templates in `web/components/templates/`.

### Authentication

JWT-based authentication using cookies:
- Token generation and validation: `auth/token/token.go`
- Token claims structure: `auth/token/claim.go`
- User authentication service: `user/services/services.go`
- Configuration via environment variables in `internal/config/config.go`:
  - `APP_PRIVATE_KEY`: JWT signing key (default: "VERY_PRIVATE_KEY")
  - `TOKEN_TTL`: Token time-to-live in nanoseconds (default: 300000)

### Database

SQLite database managed via `internal/database/engine.go`:
- Database file: `akingbee.db` (created automatically)
- Singleton pattern ensures single connection
- Migrations in `internal/database/queries/migrations/` (applied on startup)
- Each migration in separate folder (M0001/, M0002/, etc.)

### Page Rendering

The `web/` directory contains shared components and page building:
- `web/pages/builder.go`: Full page assembly with authenticated/unauthenticated states
- `web/components/`: Reusable UI components (buttons, forms, modals, tables, notifications)
- `web/helpers.go`: Template rendering utilities

Components use Go's `html/template` for server-side rendering.

## Development Environment

The project uses Nix for environment management (see `shell.nix`):
- Go 1.22.5
- golangci-lint for linting
- sqlite for database
- air for hot reloading (optional)

Load with: `nix-shell` or `direnv allow`

## Key Patterns

### Public IDs
All entities use UUID-based public IDs (via `github.com/google/uuid`) for external references, keeping internal database IDs private.

### Error Handling
Services and repositories return Go errors. HTTP handlers log errors and return appropriate status codes. Authentication failures return 401, general errors typically 500.

### Repository Pattern
Repositories provide data access abstraction. They accept `context.Context` and return domain models or errors. Database queries use `database/sql` with SQLite driver.

### Service Layer
Services contain business logic and coordinate between repositories. They enforce authorization rules and data validation before persisting changes.

## Important Notes

- The main branch is `master` (not main)
- CI runs on all branches via GitHub Actions (`.github/workflows/akingbee.yaml`)
- Releases trigger Docker image builds (`.github/workflows/release.yaml`)
- The application auto-runs migrations on startup in `akingbee.go`
- Public resources (CSS, JS, images) served from `web/resources/` via `/public/` path
