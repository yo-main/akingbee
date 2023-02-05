#!/usr/bin/env sh

if [ "$EXECUTE_MIGRATION" ]; then
  alembic upgrade head
fi

exec "$@"
