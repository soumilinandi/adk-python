# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any
from typing import Dict
from typing import List

from adk_release_analyzer.settings import GITHUB_TOKEN
import requests

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}


def error_response(error_message: str) -> Dict[str, Any]:
  return {"status": "error", "error_message": error_message}


def get_request(
    url: str,
    headers: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
) -> Dict[str, Any]:
  """Executes a GET request."""
  if headers is None:
    headers = HEADERS
  if params is None:
    params = {}
  response = requests.get(url, headers=headers, params=params, timeout=60)
  response.raise_for_status()
  return response.json()


def get_paginated_request(
    url: str, headers: dict[str, Any] | None = None
) -> List[Dict[str, Any]]:
  """Executes GET requests and follows 'next' pagination links to fetch all results."""
  if headers is None:
    headers = HEADERS

  results = []
  while url:
    response = requests.get(url, headers=headers, timeout=60)
    response.raise_for_status()
    results.extend(response.json())
    url = response.links.get("next", {}).get("url")
  return results


def post_request(url: str, payload: Any) -> Dict[str, Any]:
  response = requests.post(url, headers=HEADERS, json=payload, timeout=60)
  response.raise_for_status()
  return response.json()


def patch_request(url: str, payload: Any) -> Dict[str, Any]:
  response = requests.patch(url, headers=HEADERS, json=payload, timeout=60)
  response.raise_for_status()
  return response.json()
