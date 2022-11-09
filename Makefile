

.PHONY: shell
shell: 
	@poetry run ipython

	
run_server:
	@poetry run uvicorn controllers.api.bee.app:create_app --port 9001 --reload --app-dir src/
	
make test:
	@poetry run pytest

remove_pyc:
	@echo Removing .pylocalc files !
	@find .  -name '*.pyc' -delete
