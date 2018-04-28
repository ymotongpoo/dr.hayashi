#    Copyright 2018 ymotongpoo
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import concurrent.futures
import logging
import urllib.request
import os.path

MAX_PAGE = 6886
DR_HAYASHI_URL = "http://kokoro.squares.net/?p={}"

def init_logger():
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter("[%(asctime)s][%(threadName)s] %(message)s"))
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def task(num):
    logging.getLogger().info("[page %s] start", num)
    req = urllib.request.Request(DR_HAYASHI_URL.format(num))
    try:
        with urllib.request.urlopen(req) as resp:
            page = resp.read()
            filename = os.path.join("data", "{}.html".format(num))
            with open(filename, 'wb') as fp:
                fp.write(filename)
    except urllib.request.HTTPError as e:
        logging.getLogger().warning("[page %s] %s", num, e)
    logging.getLogger().info("[page %s] end", num)


def main():
    init_logger()
    logging.getLogger().info("start process")
    with concurrent.futures.ThreadPoolExecutor(max_workers=8, thread_name_prefix="thread") as executor:
        results = executor.map(task, range(MAX_PAGE))
        logging.getLogger().info("map end")
    logging.getLogger().info(list(results))
    logging.getLogger().info("end process")
