#!/bin/bash

# Determine which set lines should be used - https://gist.github.com/mohanpedala/1e2ff5661761d3abd0385e8223e16425
#
# set -e            fail if any command has a non-zero exit
# set -u            fail if referencing an undefined variable 
# set -o pipefail   prevent errors in a pipeline from being masked (if any command in pipeline fails that return code will be used)
# set -x            all executed commands are printed to terminal (should not be used unless debugging)

set -eo pipefail

SCRIPT_DIR=$(dirname "$0")
exe() { echo -e "\$ $@\n" ; "$@" ; }

help() {

   # Display Help
    echo "cURL a file or directory of file bundles to a FHIR endpoint"
    echo
    echo "Usage: $0 [-v] -u <url> -t <token> [-f <file>] [-d <directory>]"
    echo "options:"
    echo "  v                      Verbose output"
    echo "  u                      URL to send bundle.  Defaults to https://bend.local.commure.com:8000/api/v1/r4"
    echo "  m                      Method to use.  Defaults to POST"
    echo "  t                      Bearer token required by endpoint"
    echo "  f <file>               File containing bundle to send"
    echo "  d <directory>          Directory containing bundles to send"
    echo
    echo "Example: ./fhir-curl -t {{TOKEN}} -f cleanup/identifier00.json"

}

run_curl() {
    if [[ x"$VERBOSE" != x ]]; then
        printf "cURLing $1\n"
        exe curl "${curl_opts[@]}" \
            -i \
            --data "@$1" $URL
        printf "\n\n"
    else
        response=$(curl "${curl_opts[@]}" \
                --data "@${1}" \
                -o /dev/null \
                -w '%{http_code}' $URL)
        case "$response" in
                200) printf "%-110s | %-8s | %-20s\n" $1 $METHOD "$response OK";;
                400) printf "%-110s | %-8s | %-20s\n" $1 $METHOD "$response Not found";;
                405) printf "%-110s | %-8s | %-20s\n" $1 $METHOD "$response Not Allowed";;
                *) printf "%-110s | %-8s | %-20s\n" $1 $METHOD "$response Exception Occurred";;
        esac    
    fi
}

while getopts u:d:f:t:v opt; do
    case "${opt}" in
        u) URL=${OPTARG} ;;
        m) METHOD=${OPTARG} ;;
        t) TOKEN=${OPTARG} ;;
        f) FILE=${OPTARG} ;;
        d) DIRECTORY=${OPTARG} ;;
        v) VERBOSE="true" ;;
        ?) help ;; # Print usage for invalid param
    esac
done

if [[ x"$URL" = x ]]; then
    URL="https://localhost:8000/api/v1/r4"
fi

# Set cURL options
curl_opts+=(--request "${METHOD}")
curl_opts+=(--silent --show-error --location --insecure ) #-sSLk
curl_opts+=(--header "Authorization: Bearer ${TOKEN}")
curl_opts+=(--header "Content-Type: application/json")

if [[ x"$VERBOSE" = x ]]; then
    printf "%-110s | %-8s | %-20s\n" "FILE" "METHOD" "RESULT"
    printf "%-110s | %-8s | %-20s\n" "-----------" ""--------" ""-----------"
fi

if [[ x"$DIRECTORY" != x ]]; then
    for f in $(find ${DIRECTORY} -type f | sort); do
        run_curl $f
        sleep 3s
    done
else
    run_curl $FILE
fi

