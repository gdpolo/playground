from os.path import exists

from src.local_search.local_search import LocalSearch
from src.utils.log_time import log_time
from flask import Flask, request

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.

app = Flask(__name__)

@log_time
def _init_search_engine(root_dir: str, search_index_path: str, force_build_index=False):
    local_search = LocalSearch()
    if force_build_index or not exists(search_index_path):
        local_search.index_directory(root_dir) # todo - windows is different?
        local_search._data_store.export_to_file(search_index_path)
    else:
        local_search._data_store.import_from_file(search_index_path)

    return local_search
local_search = None

@app.route('/', methods=['GET'])
def home():
    return "Wellcome! This is your local search engine app!"

@app.route('/search', methods=['GET'])
def get():
    key_words = request.args.get('key_words')
    return local_search.search(key_words.split(","))

@app.route('/reset_index', methods=['GET'])
def reset_index():
    try:
        root_path = request.args.get('root_path')
        index_path = request.args.get('index_path')
        local_search = _init_search_engine(root_path, index_path, True)
        return "SUCCESS"
    except:
        return "ERROR"

@app.route('/load_index', methods=['GET'])
def load_index():
    try:
        index_path = request.args.get('index_path')
        local_search = _init_search_engine("/", index_path, False)
        return "SUCCESS"
    except:
        return "ERROR"

if __name__ == '__main__':
    # This is used when running locally only. When deploying
    # a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    local_search = _init_search_engine("/", "/tmp/local_search_index.json")
    app.run(host='127.0.0.1', port=8080, debug=False)
