import json
import os
import math

from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked
from dotenv import load_dotenv


def render_mode():
    '''Режим работы рендера'''
    mode = os.getenv("MODE", "github")
    if mode == "livereload":
        return "/"
    else:
        return "/online_library/"


def render_pages():
    '''Рендер страниц'''
    with open("meta_data.json", "r", encoding="utf8") as my_file:
        books = json.load(my_file)

    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html"])
    )
    env.filters["chunked"] = chunked
    template = env.get_template("template.html")

    os.makedirs("pages", exist_ok=True)
    books_per_page = 10
    chunked_books = list(chunked(books, books_per_page))
    total_pages = math.ceil(len(books) / books_per_page)
    base_path = render_mode()

    for page_num, book_chunk in enumerate(chunked_books, start=1):
        columns = [
            book_chunk[:len(book_chunk)//2],
            book_chunk[len(book_chunk)//2:]
        ]
        rendered_page = template.render(
            columns=columns,
            current_page=page_num,
            total_pages=total_pages,
            base_path=base_path,
        )
        with open(f"pages/index{page_num}.html", "w", encoding="utf8") as file:
            file.write(rendered_page)

    with open("index.html", "w", encoding="utf8") as file:
        file.write(open("pages/index1.html", "r", encoding="utf8").read())


def main():
    load_dotenv()
    render_pages()
    server = Server()
    server.watch("template.html", render_pages)

    server.serve(root=".", port=5500, host="127.0.0.1")


if __name__ == "__main__":
    main()
