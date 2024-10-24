from aiocache import cached
from quart import Blueprint, render_template, request, send_file
from ..converter import text_to_img_converter

converter = Blueprint("converter", __name__)


@converter.route("/converter")
@cached(ttl=3600)
async def converter_page():
    return await render_template("converter/index.html")

@converter.route("/converter", methods=["POST"])
async def convert():
    form_data = await request.form
    text = form_data.get("text", "").strip()

    if not text:
        return {"error": "Text cannot be empty."}, 400
    if len(text) > 256:
        return {"error": "Text exceeds the limit of 256 characters."}, 400

    try:
        file_path = await text_to_img_converter(text)
    except Exception as e:
        return {"error": f"Failed to generate image: {str(e)}"}, 500

    return await send_file(file_path, mimetype="image/png", as_attachment=True)
