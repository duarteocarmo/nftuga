import asyncio
import concurrent.futures
import requests
import pathlib

id_list = list(range(7500, 100_000))
good_ids = []
images_folder = pathlib.Path("images/")
# images_folder.mkdir(exist_ok=True)


def download_photo(id):
    try:
        URL = f"https://app.parlamento.pt/webutils/getimage.aspx?id={id}&type=deputado"
        response = requests.get(URL)

        if response.status_code == 200 and len(response.content) != 2573:
            good_ids.append(id)
            data = response.content

            print(response.status_code, id, len(data))
            with open(images_folder / f"{id}.png", "wb") as f:
                f.write(data)

        return None
    except Exception as e:
        print(str(e))
        return None


# parallelize requests using asyncio
async def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(executor, download_photo, id)
            for id in id_list
        ]


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
print(good_ids)
