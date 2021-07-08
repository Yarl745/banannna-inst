from environs import Env

env = Env()
env.read_env()

IG_USERNAME = env.str("IG_USERNAME")
IG_PASSWORD = env.str("IG_PASSWORD")

BOT_IP = env.str("BOT_IP")

PG_USER = env.str("PG_USER")
PG_PASSWORD = env.str("PG_PASSWORD")
PG_DB = env.str("PG_DB")
PG_PORT = env.str("PG_PORT")

WEBHOOK_SSL_CERT = "webhook_cert.pem"
WEBHOOK_SSL_PKEY = "webhook_pkey.pem"

REDIS_PASS = env.str("REDIS_PASS")

BOT_PORT = env.str("BOT_PORT")
CONTROLLER_PORT = env.str("CONTROLLER_PORT")

BOT_HOST = f"https://{BOT_IP}:{BOT_PORT}"
CONTROLLER_HOST = f"https://{BOT_IP}:{CONTROLLER_PORT}"

