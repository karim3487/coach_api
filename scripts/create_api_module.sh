#!/bin/bash

# module name (profiles, workouts)
MODULE_NAME=$1

# base path
BASE_PATH="apps/api/v1"

# dir of module
MODULE_PATH="$BASE_PATH/$MODULE_NAME"

mkdir -p "$MODULE_PATH"

touch "$MODULE_PATH/__init__.py"
touch "$MODULE_PATH/views.py"
touch "$MODULE_PATH/serializers.py"
touch "$MODULE_PATH/urls.py"
touch "$MODULE_PATH/filters.py"

echo "API module '$MODULE_NAME' created at $MODULE_PATH"
