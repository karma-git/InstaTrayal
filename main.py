from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from instagrapi import Client
import logging
import json
from pprint import pformat

# Настраиваем логирование
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI()

# TODO: any other option to authorize?
class UserCredentials(BaseModel):
    username: str
    password: str

@app.post("/unfollowers/")
async def get_unfollowers(credentials: UserCredentials):
    logger.debug(f"Hello Logger")
    cl = Client()
    try:
        cl.login(credentials.username, credentials.password)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Ошибка авторизации: {}".format(e))

    user_id = cl.user_id_from_username(credentials.username)
    following = cl.user_following(user_id)
    followers = cl.user_followers(user_id)

    unfollowers = {}
    for user in following.values():
        if user.pk not in followers:
            unfollower = {user.username: user.full_name}
            unfollowers.update(unfollower)

    unfollowers_json = json.dumps(unfollowers, indent=4, ensure_ascii=False)
    logger.debug(f"Последний отписун {user} {dir(user)}")
    logger.debug(f"Отписуны: {unfollowers}")

    return {"unfollowers": unfollowers}
