import json

from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape


def render_page():
    with open("meta_data.json", "r", encoding="utf8") as my_file:
        books = json.load(my_file)

    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html"])
    )
    template = env.get_template("template.html")
    page = template.render(books=books)

    with open("index.html", "w", encoding="utf8") as file:
        file.write(page)


render_page()

server = Server()
server.watch("template.html", render_page)

server.serve(root=".", port=5500, host="0.0.0.0")
