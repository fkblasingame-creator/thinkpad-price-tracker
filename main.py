from trackers.craigslist import search
from models import SEARCH_MODELS


def main():
    for model in SEARCH_MODELS:
        print("=" * 60)
        print(model["name"])
        print("=" * 60)

        results = search(model["search"])
        excluded = model.get("excluded", [])
        required = model.get("required", [])
        filtered_results = []   

        print(f"Found {len(results)} listings.\n")

        for item in results:
            title = item["title"].lower()
            if any(keyword in title for keyword in excluded):
                continue
            if item["price"] > model["max_price"]:
                continue
            if required and not all(keyword.lower() in title for keyword in required):
                continue
            filtered_results.append(item)

        print(f"Found {len(filtered_results)} listings after filtering.\n")

        for item in filtered_results:
            print(item["price"])
            print(item["title"])
            print(item["location"])
            print(item["url"])
            print("-" * 60)


if __name__ == "__main__":
    main()