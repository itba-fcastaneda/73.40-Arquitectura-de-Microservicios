from flask import Flask
from healthcheck import HealthCheck, EnvironmentDump
import redis
from redis.exceptions import TimeoutError as RedisTimeoutError

app = Flask(__name__)

health = HealthCheck()
envdump = EnvironmentDump()

# add your own check function to the healthcheck
def redis_available():
    status = False
    reason = "redis ok"
    try:
        client = redis.Redis(
            host="localhost",
            socket_timeout=5
        )
        info = client.info()
    except RedisTimeoutError :
        reason = "redis timeout"
    except:
        reason = "redis error"
    
    return status, reason

health.add_check(redis_available)

# add your own data to the environment dump
def application_data():
    return {"owner": "Team A"}

envdump.add_section("application", application_data)

# Add a flask route to expose information
app.add_url_rule("/healthcheck", "healthcheck", view_func=lambda: health.run())
app.add_url_rule("/environment", "environment", view_func=lambda: envdump.run())