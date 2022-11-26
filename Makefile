
pass ?=


.PHONY: shell
shell: 
	@poetry run ipython

	
run_server:
	@poetry run uvicorn controllers.api.bee.app:create_app --port 9001 --reload --app-dir src/
	
test:
	@poetry run pytest -s tests $(pass)

remove_pyc:
	@echo Removing .pylocalc files !
	@find .  -name '*.pyc' -delete
	
%:
    @:
