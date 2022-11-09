from fastapi.middleware.cors import CORSMiddleware


def configure_cors_middleware(
    app,
    allow_origins=None,
    allow_origin_regex=None,
    allow_methods=None,
    allow_headers=None,
    allow_credentials=False,
):
    params = dict(
        allow_methods=allow_methods or ["*"],
        allow_headers=allow_headers or ["*"],
        allow_credentials=allow_credentials,
    )

    if allow_origin_regex:
        params["allow_origin_regex"] = allow_origin_regex
    else:
        params["allow_origins"] = allow_origins or ["*"]

    app.add_middleware(CORSMiddleware, **params)
