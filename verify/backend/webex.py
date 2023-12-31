#!/usr/bin/env python
"""Verify the Cisco Webex APIs are accessible and responding.

Verify that user's provide WEBEX_ACCESS_TOKEN is valid and that calls to the
Cisco Webex (formerly Spark) APIs complete successfully. Uses SPARK_
for variable names; the product name is Cisco Webex.


Copyright (c) 2018-21 Cisco and/or its affiliates.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import os
import sys

import webexteamssdk


# Get the absolute path for the directory where this file is located "here"
here = os.path.abspath(os.path.dirname(__file__))

# Get the absolute path for the project / repository root
project_root = os.path.abspath(os.path.join(here, "../.."))

# Extend the system path to include the project root and import the env files
if project_root not in sys.path:
    sys.path.insert(0, project_root)


import env_user  # noqa


def verify() -> bool:
    """Verify access to the Cisco Webex APIs."""
    print("==> Verifying access to the Cisco Webex APIs")

    # Check to ensure the user has provided their Webex Access Token
    if not env_user.WEBEX_ACCESS_TOKEN:
        print(
            "\nFAILED: You must provide your WEBEX_ACCESS_TOKEN in the "
            "env_user.py file.\n"
        )
        return False

    webexapi = webexteamssdk.WebexTeamsAPI(
        access_token=env_user.WEBEX_ACCESS_TOKEN
    )

    # Verify the Cisco Webex APIs are accessible and responding
    try:
        me = webexapi.people.me()
    except webexapi.WebexApiError as e:
        print(
            "\nFAILED: The API call to Cisco Webex returned the following "
            "error:\n{}\n".format(e)
        )
        return False

    else:
        print(
            "\nYou are connected to Cisco Webex (formerly Webex) as: {}\n".format(me.emails[0])
        )

    # Check to ensure the user has provided a Webex Room ID
    if not env_user.WEBEX_ROOM_ID:
        print(
            "\nFAILED: You must provide the WEBEX_ROOM_ID of the room you "
            "want to work with in the env_user.py file.\n"
        )
        return False

    # Verify the Webex Room exists and is accessible via the access token
    try:
        room = webexapi.rooms.get(env_user.WEBEX_ROOM_ID)
    except webexapi.WebexApiError as e:
        print(
            "\nFAILED: There was an error accessing the Webex Room using the "
            "WEBEX_ROOM_ID you provided; error details:\n{}\n".format(e)
        )
        return False
    else:
        print(
            "You will be posting messages to the following room: '{}'\n"
            "".format(room.title)
        )

    return True


if __name__ == '__main__':
    verify()
