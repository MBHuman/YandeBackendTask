# encoding=utf8

import json
import re
import subprocess
import sys
from urllib import response
import urllib.error
import urllib.parse
import urllib.request

API_BASEURL = "http://localhost:80"

ROOT_ID = "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
ROOT_ID_2 = "23f3dafa-ff44-4d09-a489-38e14725f5f1"
ROOT_ID_3 = "98883e8f-0507-482f-bce2-2fb306cf6483"
ROOT_ID_4 = "d515e43f-f3f6-4471-bb77-6b455017a2d2"
ROOT_ID_5 = "863e1a7a-1304-42ae-943b-179184c077e3"

ERROR_IMPORTS = [
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Товары",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "parentId": None,
                "price": None
            },
            {
                "type": "CATEGORY",
                "name": "Товары",
                "id": "dc8d73c3-e0c0-41df-8c6d-7e654930ce87",
                "parentId": None,
                "price": 10
            }
        ],
        "updateDate": "2022-02-01T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Товары",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "parentId": None
            },
            {
                "type": "CATEGORY",
                "name": "Товары",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "parentId": None
            }
        ],
        "updateDate": "2022-02-01T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "OFFER",
                "name": "Товары",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "parentId": None,
                "price": 3
            },
            {
                "type": "OFFER",
                "name": "Товары",
                "id": "053a716c-4ade-4747-be87-3cd3891403fb",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "price": 6
            }
        ],
        "updateDate": "2022-02-01T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "OFFER",
                "name": "Товары",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "parentId": None,
                "price": 3
            },
            {
                "type": "OFFER",
                "name": None,
                "id": "053a716c-4ade-4747-be87-3cd3891403fb",
                "parentId": None,
                "price": 6
            }
        ],
        "updateDate": "2022-02-01T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "OFFER",
                "name": "Товары",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "parentId": None,
                "price": 3
            },
            {
                "type": "OFFER",
                "name": "Товары",
                "id": "053a716c-4ade-4747-be87-3cd3891403fb",
                "parentId": None,
                "price": None
            }
        ],
        "updateDate": "2022-02-01T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "OFFER",
                "name": "Товары",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "parentId": None,
                "price": 3
            },
            {
                "type": "OFFER",
                "name": "Товары",
                "id": "053a716c-4ade-4747-be87-3cd3891403fb",
                "parentId": None,
                "price": -1
            }
        ],
        "updateDate": "2022-02-01T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "OFFER",
                "name": "Товары",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "parentId": None,
                "price": 3
            },
            {
                "type": "OFFER",
                "name": "Товары",
                "id": "053a716c-4ade-4747-be87-3cd3891403fb",
                "parentId": None,
                "price": 6
            }
        ],
        "updateDate": "2022-59-01T12:00:00.000Z"
    },
]

IMPORT_BATCHES = [
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Товары",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "parentId": None
            }
        ],
        "updateDate": "2022-02-01T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Смартфоны",
                "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
            },
            {
                "type": "OFFER",
                "name": "jPhone 13",
                "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "price": 79999
            },
            {
                "type": "OFFER",
                "name": "Xomiа Readme 10",
                "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "price": 59999
            }
        ],
        "updateDate": "2022-02-02T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Телевизоры",
                "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
            },
            {
                "type": "OFFER",
                "name": "Samson 70\" LED UHD Smart",
                "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 32999
            },
            {
                "type": "OFFER",
                "name": "Phyllis 50\" LED UHD Smarter",
                "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 49999
            }
        ],
        "updateDate": "2022-02-03T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "OFFER",
                "name": "Goldstar 65\" LED UHD LOL Very Smart",
                "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 69999
            }
        ],
        "updateDate": "2022-02-03T15:00:00.000Z"
    },
    {

        "items": [
            {
                "id": "23f3dafa-ff44-4d09-a489-38e14725f5f1",
                "name": "Категория",
                "parentId": None,
                "type": "CATEGORY",
                "price": None
            }
        ],
        "updateDate": "2002-05-28T21:12:01.000Z"
    },
    {
        "items": [
            {
                "id": "9980d216-b43c-4310-bbf0-169220aeea2b",
                "name": "Категория",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "type": "CATEGORY",
                "price": None
            }
        ],
        "updateDate": "2002-06-28T21:12:01.000Z"
    }
]

IMPORT_UPDATE_PARENT = {
    "items": [
        {
            "type": "OFFER",
            "name": "jPhone 13",
            "id": "863e1a7a-1304-42ae-943b-179184c077e3",
            "parentId": None,
            "price": 79999
        }
    ],
    "updateDate": "2022-02-02T12:00:00.000Z"
}

IMPORT_UPDATE_PARENT_2 = {
    "items": [
        {
            "type": "OFFER",
            "name": "jPhone 13",
            "id": "863e1a7a-1304-42ae-943b-179184c077e3",
            "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
            "price": 79999
        }
    ],
    "updateDate": "2022-02-02T12:00:00.000Z"
}

EXPECTED_TREE = {
    "type": "CATEGORY",
    "name": "Товары",
    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
    "price": 58599,
    "parentId": None,
    "date": "2002-06-28T21:12:01.000Z",
    "children": [
        {
            "type": "CATEGORY",
            "name": "Телевизоры",
            "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "price": 50999,
            "date": "2022-02-03T15:00:00.000Z",
            "children": [
                {
                    "type": "OFFER",
                    "name": "Samson 70\" LED UHD Smart",
                    "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 32999,
                    "date": "2022-02-03T12:00:00.000Z",
                    "children": None,
                },
                {
                    "type": "OFFER",
                    "name": "Phyllis 50\" LED UHD Smarter",
                    "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 49999,
                    "date": "2022-02-03T12:00:00.000Z",
                    "children": None
                },
                {
                    "type": "OFFER",
                    "name": "Goldstar 65\" LED UHD LOL Very Smart",
                    "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 69999,
                    "date": "2022-02-03T15:00:00.000Z",
                    "children": None
                }
            ]
        },
        {
            "type": "CATEGORY",
            "name": "Смартфоны",
            "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "price": 69999,
            "date": "2022-02-02T12:00:00.000Z",
            "children": [
                {
                    "type": "OFFER",
                    "name": "jPhone 13",
                    "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "price": 79999,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                },
                {
                    "type": "OFFER",
                    "name": "Xomiа Readme 10",
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "price": 59999,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                }
            ]
        },
        {

            "id": "9980d216-b43c-4310-bbf0-169220aeea2b",
            "name": "Категория",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "type": "CATEGORY",
            "price": None,
            "date": "2002-06-28T21:12:01.000Z",
            "children": []
        }
    ]
}

EXPECTED_TREE_2 = {
    "id": "23f3dafa-ff44-4d09-a489-38e14725f5f1",
    "name": "Категория",
    "parentId": None,
    "type": "CATEGORY",
    "price": None,
    "date": "2002-05-28T21:12:01.000Z",
    "children": []
}

EXPECTED_TREE_3 ={
    "type": "CATEGORY",
    "name": "Смартфоны",
    "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
    "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
    "price": 59999,
    "date": "2022-02-02T12:00:00.000Z",
    "children": [
        {
            "type": "OFFER",
            "name": "Xomiа Readme 10",
            "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
            "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
            "price": 59999,
            "date": "2022-02-02T12:00:00.000Z",
            "children": None
        }
    ]
}

EXPECTED_TREE_4 = {
    "type": "OFFER",
    "name": "jPhone 13",
    "id": "863e1a7a-1304-42ae-943b-179184c077e3",
    "parentId": None,
    "price": 79999,
    "date": "2022-02-02T12:00:00.000Z",
    "children": None
}


EXPECTED_SALES_TREE = {
    "items": [
        {
            "type": "OFFER",
            "name": "jPhone 13",
            "id": "863e1a7a-1304-42ae-943b-179184c077e3",
            "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
            "price": 79999,
            "date": "2022-02-02T12:00:00.000Z",
        },
        {
            "type": "OFFER",
            "name": "Xomiа Readme 10",
            "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
            "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
            "price": 59999,
            "date": "2022-02-02T12:00:00.000Z",
        }
    ]
}


def request(path, method="GET", data=None, json_response=False):
    try:
        params = {
            "url": f"{API_BASEURL}{path}",
            "method": method,
            "headers": {},
        }

        if data:
            params["data"] = json.dumps(
                data, ensure_ascii=False).encode("utf-8")
            params["headers"]["Content-Length"] = len(params["data"])
            params["headers"]["Content-Type"] = "application/json"

        req = urllib.request.Request(**params)

        with urllib.request.urlopen(req) as res:
            res_data = res.read().decode("utf-8")
            if json_response:
                res_data = json.loads(res_data)
            return (res.getcode(), res_data)
    except urllib.error.HTTPError as e:
        return (e.getcode(), None)


def deep_sort_children(node):
    if node.get("children"):
        node["children"].sort(key=lambda x: x["id"])

        for child in node["children"]:
            deep_sort_children(child)


def sort_elems(node):
    node['items'].sort(key=lambda x: x["id"])


def print_diff(expected, response):
    with open("expected.json", "w") as f:
        json.dump(expected, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")

    with open("response.json", "w") as f:
        json.dump(response, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")

    subprocess.run(["git", "--no-pager", "diff", "--no-index",
                    "expected.json", "response.json"])


def test_import():

    for index, batch in enumerate(ERROR_IMPORTS):
        print(f"Importing batch {index}")
        status, _ = request("/imports", method="POST", data=batch)

        assert status == 400, f"Expected HTTP status code 400, got {status}"

    for index, batch in enumerate(IMPORT_BATCHES):
        print(f"Importing batch {index}")
        status, _ = request("/imports", method="POST", data=batch)

        assert status == 200, f"Expected HTTP status code 200, got {status}"

    print("Test import passed.")


def test_nodes():
    status, response = request(f"/nodes/{ROOT_ID}", json_response=True)
    # print(json.dumps(response, indent=2, ensure_ascii=False))

    assert status == 200, f"Expected HTTP status code 200, got {status}"

    deep_sort_children(response)
    deep_sort_children(EXPECTED_TREE)
    if response != EXPECTED_TREE:
        print_diff(EXPECTED_TREE, response)
        print("Response tree doesn't match expected tree.")
        sys.exit(1)

    status, response = request(f"/nodes/{ROOT_ID_2}", json_response=True)

    assert status == 200, f"Expected HTTP status code 200, got {status}"

    deep_sort_children(response)
    deep_sort_children(EXPECTED_TREE_2)
    if response != EXPECTED_TREE_2:
        print_diff(EXPECTED_TREE_2, response)
        print("Response tree doesn't match expected tree.")
        sys.exit(1)

    print("Test nodes passed.")


def test_sales():
    params = urllib.parse.urlencode({
        "date": "2022-02-02T13:00:00.000Z"
    })
    status, response = request(f"/sales?{params}", json_response=True)
    assert status == 200, f"Expected HTTP status code 200, got {status}"
    sort_elems(response)
    sort_elems(EXPECTED_SALES_TREE)
    if response != EXPECTED_SALES_TREE:
        print_diff(EXPECTED_SALES_TREE, response)
        print("Response tree doesn't match expected tree.")
        sys.exit(1)

    print("Test sales passed.")


def test_stats():
    params = urllib.parse.urlencode({
        "dateStart": "2022-02-01T00:00:00.000Z",
        "dateEnd": "2022-02-03T00:00:00.000Z"
    })
    status, response = request(
        f"/node/{ROOT_ID}/statistic?{params}", json_response=True)

    assert status == 200, f"Expected HTTP status code 200, got {status}"
    print("Test stats passed.")

def test_import_second():

    status, _ = request("/imports", method="POST", data=IMPORT_UPDATE_PARENT)
    assert status == 200, f"Expected HTTP status code 200, got {status}"

    status, response = request(f"/nodes/{ROOT_ID_4}", json_response=True)
    if response != EXPECTED_TREE_3:
        print_diff(EXPECTED_TREE_3, response)
        print("Response tree doesn't match expected tree.")
        sys.exit(1)
    
    status, response = request(f"/nodes/{ROOT_ID_5}", json_response=True)
    if response != EXPECTED_TREE_4:
        print_diff(EXPECTED_TREE_4, response)
        print("Response tree doesn't match expected tree.")
        sys.exit(1)


    print("Test import second passed.")

def test_delete():
    status, _ = request(f"/delete/{ROOT_ID}", method="DELETE")
    assert status == 200, f"Expected HTTP status code 200, got {status}"

    status, _ = request(f"/nodes/{ROOT_ID}", json_response=True)
    assert status == 404, f"Expected HTTP status code 404, got {status}"

    status, _ = request(f"/nodes/{ROOT_ID_3}", json_response=True)
    assert status == 404, f"Expected HTTP status code 404, got {status}"

    print("Test delete passed.")


def test_all():
    test_import()
    test_nodes()
    test_sales()
    test_stats()
    test_import_second()
    test_delete()


def main():
    global API_BASEURL
    test_name = None

    for arg in sys.argv[1:]:
        if re.match(r"^https?://", arg):
            API_BASEURL = arg
        elif test_name is None:
            test_name = arg

    if API_BASEURL.endswith('/'):
        API_BASEURL = API_BASEURL[:-1]

    if test_name is None:
        test_all()
    else:
        test_func = globals().get(f"test_{test_name}")
        if not test_func:
            print(f"Unknown test: {test_name}")
            sys.exit(1)
        test_func()


if __name__ == "__main__":
    main()
