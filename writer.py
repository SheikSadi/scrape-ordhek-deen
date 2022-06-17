import os
from scraper import scrape


def write():
    with open("last biodata_number.txt", "r") as fp:
        biodata_number = int(
            fp.read()
        )

    while biodata_number:
        biodata_number -= 1

        fname = f"data/{biodata_number}.json"

        if os.path.isfile(fname):
            continue

        document = scrape(biodata_number)

        if document:
            with open(fname, "w") as fp:
                fp.write(document)

            with open("last biodata_number.txt", "w") as fp:
                fp.write(
                    str(biodata_number)
                )
        break

if __name__ == "__main__":
    if not os.path.isdir("data"):
        os.mkdir("data")
    write()
