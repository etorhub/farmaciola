DOMAIN = "farmaciola"
STORAGE_VERSION = 1
STORAGE_KEY = f"{DOMAIN}.medicines"
STORAGE_NOTIFICATION_SETTINGS_KEY = f"{DOMAIN}.notification_settings"
CIMA_BASE_URL = "https://cima.aemps.es/cima/rest"
DEFAULT_NOTIFY_SERVICE = "notify.notify"
CONF_NOTIFY_SERVICE = "notify_service"

DEFAULT_NOTIFICATION_SETTINGS = {
    "enabled": True,
    "notify_persistent": True,
    "notify_mobile": True,
    "notify_service": DEFAULT_NOTIFY_SERVICE,
}
