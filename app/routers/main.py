from quart import Blueprint, render_template
from aiocache import cached

main = Blueprint("main", __name__)

@main.route("/")
@cached(ttl=3600)
async def index():
    return await render_template("main/index.html")
