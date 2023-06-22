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
