import json
import os
import math
from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked


def is_github_pages():
    '''Определяем, работает ли скрипт на GitHub Pages'''
    return os.path.exists('/github/workspace') or 'GITHUB_ACTIONS' in os.environ


def get_base_url():
    """Автоматически определяет правильный base_url"""
    # Для GitHub Pages (ваш репозиторий: online_library)
    if os.path.exists('/github/workspace') or 'GITHUB_ACTIONS' in os.environ:
        return "/online_library"
    # Для локального запуска
    return ""


def main():
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

        base_url = get_base_url()

        for page_num, book_chunk in enumerate(chunked_books, start=1):
            columns = [book_chunk[:len(book_chunk)//2], book_chunk[len(book_chunk)//2:]]

            rendered_page = template.render(
                columns=columns,
                current_page=page_num,
                total_pages=total_pages,
                base_url=base_url
            )

            with open(f"pages/index{page_num}.html", "w", encoding="utf8") as file:
                file.write(rendered_page)

        # Главная страница (особый случай)
        with open("index.html", "w", encoding="utf8") as file:
            content = open("pages/index1.html", "r", encoding="utf8").read()
            # Для главной страницы делаем base_url пустым
            content = content.replace('href="{{ base_url }}/', 'href="')
            file.write(content)

    render_pages()
    server = Server()
    server.watch("template.html", render_pages)
    server.serve(root=".", port=5500, host="127.0.0.1")


if __name__ == "__main__":
    main()
