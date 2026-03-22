# VideoHub Python SDK

Official Python SDK for **VideoHub** – build video calls, audio rooms, and real-time communication applications easily.

VideoHub helps developers integrate **video conferencing, audio rooms, screen sharing, and real-time communication** into their applications with simple APIs.

---

## Installation

Install the SDK from PyPI:

```bash
pip install videohub-python
```

---

## Requirements

* Python **3.9+**
* VideoHub API Key
* App credentials (App ID & App Secret)

---

## Quick Start

```python
from videohub import VideoHubClient, VideoHubConfig

config = VideoHubConfig(
    api_key="vhub_live_xxxxxxxxx",
    app_id="your_app_id",
    app_secret="your_app_secret",
    app_platform="web",
    app_identifier="example.com"
)

client = VideoHubClient(config)

# Example: create a room token
token = client.rooms.create_token(
    room_name="my-room",
    user_id="user_123"
)

print(token)
```

---

## Authentication

All requests require the following credentials:

| Field          | Description                          |
| -------------- | ------------------------------------ |
| API Key        | Account authentication key           |
| App ID         | Unique application identifier        |
| App Secret     | Secret used for request verification |
| App Platform   | `web`, `android`, or `ios`           |
| App Identifier | Domain or package name               |

Example configuration:

```python
config = VideoHubConfig(
    api_key="vhub_live_xxxxx",
    app_id="app_uuid",
    app_secret="secret_xxxxx",
    app_platform="web",
    app_identifier="example.com"
)
```

---

## Features

The VideoHub Python SDK supports:

* Video calling
* Audio rooms
* Screen sharing
* Room management
* Call management
* Admin APIs
* Secure authentication

---

## Example: Create Room

```python
room = client.rooms.create(
    room_name="demo-room",
    max_participants=5
)

print(room)
```

---

## Example: Generate User Token

```python
token = client.rooms.create_token(
    room_name="demo-room",
    user_id="user_123"
)

print(token)
```

---

## Error Handling

The SDK raises structured exceptions for API errors.

```python
from videohub.exceptions import VideoHubError

try:
    client.rooms.create("room1")
except VideoHubError as e:
    print(e)
```

---

## Project Structure

```
videohub/
│
├── client.py
├── config.py
├── constants.py
├── exceptions.py
├── http.py
│
├── services/
│   ├── auth.py
│   ├── rooms.py
│   ├── calls.py
│   └── admin.py
│
└── utils/
    └── validators.py
```

---

## Documentation

Full API documentation is available at:

https://docs.videohub.askjitendra.com

---

## Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch
3. Submit a pull request

---

## Reporting Issues

If you encounter a bug or want to request a feature, please open an issue:

https://github.com/letscms/videohub-python/issues

---

## License

This project is licensed under the **MIT License**.
