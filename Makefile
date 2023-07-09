#################### PACKAGE ACTIONS ###################

reinstall_package:
	@pip uninstall -y wildfaire || :
	@pip install -e .

run_api:
	uvicorn wildfaire.api.fast:app --reload


run_data:
	python -c 'from wildfaire.interface.main import preprocess; data()'

run_preprocess:
	python -c 'from wildfaire.interface.main import preprocess; preprocess()'

run_train:
	python -c 'from wildfaire.interface.main import train; train()'

run_pred:
	python -c 'from wildfaire.interface.main import pred; pred()'

run_evaluate:
	python -c 'from wildfaire.interface.main import evaluate; evaluate()'

run_all: run_preprocess run_train run_pred run_evaluate

run_api_container:
	docker run -e PORT=8000 -p 8000:8000 --env-file .env $$GCR_REGION/$$GCP_PROJECT/$$GCR_API_IMAGE:prod

docker_build:
	docker build -t $GCR_REGION/$GCP_PROJECT/$GCR_API_IMAGE:prod .


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


################### DATA SOURCES ACTIONS ################

# Data sources: targets for monthly data imports
ML_DIR=~/Documents/GitHub/Wildfaire/wildfaire/ML_logic
HTTPS_DIR=https://console.cloud.google.com/storage/browser/wildfaire_data
GS_DIR=gs://wildfaire_data

show_sources_all:
	-ls -laR ~/Documents/GitHub/Wildfaire/wildfaire/ML_logic
	-gsutil ls gs://${BUCKET_NAME}

reset_local_files:
	rm -rf ${ML_DIR}
	mkdir -p ~/Documents/GitHub/Wildfaire/wildfaire/ML_logic/data
	mkdir ~/Documents/GitHub/Wildfaire/wildfaire/ML_logic/data/raw
	mkdir ~/Documents/GitHub/Wildfaire/wildfaire/ML_logic/data/processed
	mkdir ~/Documents/GitHub/Wildfaire/wildfaire/ML_logic/training_outputs
	mkdir ~/Documents/GitHub/Wildfaire/wildfaire/ML_logic/training_outputs/metrics
	mkdir ~/Documents/GitHub/Wildfaire/wildfaire/ML_logic/training_outputs/models
	mkdir ~/Documents/GitHub/Wildfaire/wildfaire/ML_logic/training_outputs/params

reset_local_files_with_csv_solutions: reset_local_files
	-curl ${HTTPS_DIR}solutions/data_query_fixture_2009-01-01_2015-01-01_1k.csv > ${ML_DIR}/data/raw/query_2009-01-01_2015-01-01_1k.csv
	-curl ${HTTPS_DIR}solutions/data_query_fixture_2009-01-01_2015-01-01_200k.csv > ${ML_DIR}/data/raw/query_2009-01-01_2015-01-01_200k.csv
	-curl ${HTTPS_DIR}solutions/data_query_fixture_2009-01-01_2015-01-01_all.csv > ${ML_DIR}/data/raw/query_2009-01-01_2015-01-01_all.csv
	-curl ${HTTPS_DIR}solutions/data_processed_fixture_2009-01-01_2015-01-01_1k.csv > ${ML_DIR}/data/processed/processed_2009-01-01_2015-01-01_1k.csv
	-curl ${HTTPS_DIR}solutions/data_processed_fixture_2009-01-01_2015-01-01_200k.csv > ${ML_DIR}/data/processed/processed_2009-01-01_2015-01-01_200k.csv
	-curl ${HTTPS_DIR}solutions/data_processed_fixture_2009-01-01_2015-01-01_all.csv > ${ML_DIR}/data/processed/processed_2009-01-01_2015-01-01_all.csv


reset_gcs_files:
	-gsutil rm -r gs://${BUCKET_NAME}
	-gsutil mb -p ${GCP_PROJECT} -l ${GCP_REGION} gs://${BUCKET_NAME}

reset_all_files: reset_local_files reset_bq_files reset_gcs_files


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
