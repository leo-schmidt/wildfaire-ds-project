#################### PACKAGE ACTIONS ###################

reinstall_package:
	@pip uninstall -y wildfaire || :
	@pip install -e .

run_api:
	uvicorn wildfaire.api.fast:app --reload


##################### TESTS #####################

test_api_root:
	pytest \
	tests/api/test_endpoints.py::test_root_is_up --asyncio-mode=strict -W "ignore" \
	tests/api/test_endpoints.py::test_root_returns_greeting --asyncio-mode=strict -W "ignore"

test_api_predict:
	pytest \
	tests/api/test_endpoints.py::test_predict_is_up --asyncio-mode=strict -W "ignore" \
	tests/api/test_endpoints.py::test_predict_is_dict --asyncio-mode=strict -W "ignore" \
	tests/api/test_endpoints.py::test_predict_has_key --asyncio-mode=strict -W "ignore" \
	tests/api/test_endpoints.py::test_predict_val_is_float --asyncio-mode=strict -W "ignore" \
	tests/api/test_endpoints.py::test_predict_image_is_up --asyncio-mode=strict -W "ignore"


##################### WEBSITE #####################

default: pytest

# default: pylint pytest

# pylint:
# 	find . -iname "*.py" -not -path "./tests/test_*" | xargs -n1 -I {}  pylint --output-format=colorized {}; true

pytest:
	echo "no tests"

# ----------------------------------
#         LOCAL SET UP
# ----------------------------------

install_requirements:
	@pip install -r requirements.txt

# ----------------------------------
#         HEROKU COMMANDS
# ----------------------------------

streamlit:
	-@streamlit run wildfaire/wildfaire_website/app.py


# ----------------------------------
#    LOCAL INSTALL COMMANDS
# ----------------------------------
install:
	@pip install . -U

clean:
	@rm -fr */__pycache__
	@rm -fr __init__.py
	@rm -fr build
	@rm -fr dist
	@rm -fr *.dist-info
	@rm -fr *.egg-info
	-@rm model.joblib
