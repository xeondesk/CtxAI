#!/bin/bash
WORKSPACE_ROOT=$(pwd)

pipx install uv
uv sync

echo "alias start-worker=\"cd $WORKSPACE_ROOT && uv run python -m celery -A app.celery worker -P threads -c 1 --loglevel INFO -Q dataset,dataset_summary,priority_dataset,priority_pipeline,pipeline,mail,ops_trace,app_deletion,plugin,workflow_storage,conversation,workflow,schedule_poller,schedule_executor,triggered_workflow_dispatcher,trigger_refresh_executor,retention\"" >> ~/.bashrc
echo "alias start-worker=\"cd $WORKSPACE_ROOT && make docker\"" >> ~/.bashrc
source /home/vscode/.bashrc