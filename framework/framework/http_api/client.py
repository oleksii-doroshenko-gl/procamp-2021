from requests import Session
from urllib.parse import urlparse

from typing import Optional


class Client:
    def __init__(self, server_url: str, headers: dict[str, str] = None):
        self.session = Session()
        self.base_url = urlparse(server_url)
        if headers is not None:
            self.common_headers = {**headers}
        else:
            self.common_headers = {}

    def close(self):
        self.session.close()

    def __merge_headers(self, headers: Optional[dict[str, str]] = None):
        return (
            self.common_headers
            if headers is None
            else {**self.common_headers, **headers}
        )

    def get(
        self,
        path: str,
        query: Optional[dict[str, str]] = None,
        headers: Optional[dict[str, str]] = None,
    ):
        query_string = (
            "&".join(f"{k}={v}" for k, v in query.items()) if query is not None else ""
        )
        url = self.base_url._replace(path=path, query=query_string).geturl()
        return self.session.get(url, headers=self.__merge_headers(headers))

    def post(
        self, path: str, data: Optional[str] = None, headers: dict[str, str] = None
    ):
        url = self.base_url._replace(path=path).geturl()

        return self.session.post(url, data=data, headers=self.__merge_headers(headers))

    def put(
        self, path: str, data: Optional[str] = None, headers: dict[str, str] = None
    ):
        url = self.base_url._replace(path=path).geturl()

        return self.session.put(url, data=data, headers=self.__merge_headers(headers))

    def delete(self, path: str, headers: dict[str, str] = None):
        url = self.base_url._replace(path=path).geturl()

        return self.session.delete(url, headers=self.__merge_headers(headers))
