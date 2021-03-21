#!/bin/sh

function givehelp {
    if [[ "$1" != "help" && "$1" != "--help" && "$1" != "" ]]; then
        echo "Unknown argument '$1'"
    fi
    echo "./docs.sh <task>"
    echo "<task>:"
    echo "install: install mkdocs and friends"
    echo "serve:   serve docs locally"
    echo "build:   build docs"
    echo "ship:  publish docs on GitHub pages"
}

mayrun="1"

case "$1" in
    install|serve|build|ship)
        mayrun="1";;
    *)
        mayrun="-1";;
esac

if [[ "$mayrun" == "-1" ]]; then
    givehelp "$@"
    exit
else
    command="$1"
    shift
    if [[ "$command" == "install" ]]; then
        pip3 install mkdocs
        pip3 install mkdocs-material
        pip3 install mkdocs-markdownextradata-plugin
    else
        if [[ "$command" == "ship" ]]; then
            command="gh-deploy"
        fi
    mkdocs $command "$@"
    fi
fi
