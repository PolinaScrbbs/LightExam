import asyncio
from quart import Quart

from .routers.main import main
from .routers.converter import converter


async def create_app() -> Quart:
    app = Quart(__name__)

    app.register_blueprint(main)
    app.register_blueprint(converter)

    return app


app = asyncio.run(create_app())
