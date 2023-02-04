#!/usr/bin/env bash
set -euo pipefail

IFS=$'\n\t'

# arguments:
#   - database user (string)
#   - database name (string)
#   - executed SQL code (string)
function exec_sql() {
  psql -v ON_ERROR_STOP=1 -c "${3}" -U "${1}" -d "${2}"
}

# arguments:
#   - username (also used as database name)
#   - users's password
function setup_app {
  local APP_NAME="${1}"
  local PWD="${2}"

  if [[ -z "$APP_NAME" ]]; then
    return 
  fi

  # create database
  psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -tc "SELECT 1 FROM pg_database WHERE datname = '${APP_NAME}'" | grep -q 1 || exec_sql ${POSTGRES_USER} ${POSTGRES_DB} "CREATE DATABASE ${APP_NAME}"

  # setup the newly created database
  exec_sql ${POSTGRES_USER} "${APP_NAME}" "
    DROP SCHEMA public CASCADE;
    CREATE SCHEMA IF NOT EXISTS ${APP_NAME};
    ALTER DATABASE ${APP_NAME} SET search_path TO ${APP_NAME};
  "

  # create user role
  psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -tc "SELECT 1 FROM pg_user WHERE usename = 'role_${APP_NAME}'" | grep -q 1 || exec_sql ${POSTGRES_USER} "${APP_NAME}" "CREATE ROLE role_${APP_NAME} LOGIN; GRANT ALL ON SCHEMA ${APP_NAME} TO role_${APP_NAME};"

  # create application user & grant them to assume the associated role
  psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -tc "SELECT 1 FROM pg_user WHERE usename = 'sa_${APP_NAME}'" | grep -q 1 || exec_sql ${POSTGRES_USER} "${APP_NAME}" "CREATE USER sa_${APP_NAME} LOGIN ENCRYPTED PASSWORD '${PWD}'; GRANT role_${APP_NAME} TO sa_${APP_NAME};"

  # set first application user default role to the associated role
  exec_sql "sa_${APP_NAME}" "${APP_NAME}" "
    ALTER USER sa_${APP_NAME} SET ROLE role_${APP_NAME};
  "
}

function main() {
  setup_app ${ARISTAEUS_USERNAME} ${ARISTAEUS_PASSWORD}
  setup_app ${CERBES_USERNAME} ${CERBES_PASSWORD}
  setup_app ${FIREFLY_USERNAME} ${FIREFLY_PASSWORD}
}

main
