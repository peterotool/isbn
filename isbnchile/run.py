import subprocess

import click


@click.command()
@click.option("--day", required=True, help="Day for the scrapy crawl")
def main(day):
    subprocess.check_call(["scrapy", "crawl", "books", "-a", f"day={day}"])
    subprocess.check_call(["python", "merge.py"])


if __name__ == "__main__":
    main()
