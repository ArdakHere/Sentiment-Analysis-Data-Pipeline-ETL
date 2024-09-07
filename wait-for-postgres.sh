#!/bin/bash

set -e

host="$1"
shift
cmd="$@"

echo "Waiting for PostgreSQL to be ready at $host..."

until [ "$(docker inspect --format='{{.State.Health.Status}}' $host)" == "healthy" ]; do
  echo "PostgreSQL is not healthy yet..."
  sleep 5
done

echo "PostgreSQL is healthy, running the command: $cmd"
exec $cmd
