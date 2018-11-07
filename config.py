#depoly
FLASK_HOST_IP = "127.0.0.1"
RULES_DATABASE_PATH = "RulesDatabase.db"
SAVE_DIALOG_STATE_TO_REDIS = False
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
IS_LOG_TO_FILE = False
LOG_PATH = "dialog_log.txt"
INTERNAL_SERVICE_URI_BASE = "https://servicetest.arobot.info:3001/api/services/"
INTERNAL_SERVICE_TOKEN = "YtdH2w54mYT2dt54RK0IWolrqc9muDXIupbOI9x3z5trIhKyNPwpfXLyPM2qtTjP"
ENABLE_PROXY = True
PROXY_URI = "http://tom.chen:Tc12345678@192.168.0.222:8080"

#machine learning
ENALBE_MACHINE_LEARNING = False

#classifier
JIEBA_DICT_PATH = "dict.txt"
DATA_SET_PATH = "dataset.json"
LOG_REG_ARGS = {
    "loss": "log",
    "penalty": "l2",
    "class_weight": "balanced",
    "max_iter": 5,
    "n_jobs": -1
}