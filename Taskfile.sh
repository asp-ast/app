#!/usr/bin/env bash

set -e

SERVICE="app"


dc() {
    docker compose "$@"
}


dcr() {
    dc run --rm "$SERVICE" "$@"
}


run() {
    dc up "$@"
}


poetry() {
    dcr poetry "$@"
}


manage() {
    dcr python manage.py "$@"
}


makemigrations() {
    manage makemigrations
}


migrate() {
    manage migrate
}


update-poetry-lock() {
    poetry lock --no-update
}


case "$1" in
    dc)
        shift
        dc "$@"
        ;;

    dcr)
        shift
        dcr "$@"
        ;;

    run)
        shift
        run "$@"
        ;;

    poetry)
        shift
        poetry "$@"
        ;;

    manage)
        shift
        manage "$@"
        ;;

    makemigrations)
        shift
        makemigrations "$@"
        ;;

    migrate)
        shift
        migrate "$@"
        ;;

    update-poetry-lock)
        shift
        update-poetry-lock "$@"
        ;;

    *)
        echo "Unknown command: $1"
        exit 1
        ;;
esac