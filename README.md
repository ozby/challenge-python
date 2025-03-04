# Python/MongoDB TCP Comment Server (for FUN)

A Python TCP Server implementation that mimics a comment server for videos with time marker.
It also support live notifications (via mongodb change stream) for replies and mentions (@user)

```
REQUEST_ID | ACTION | PARAMS....
ougmcim|SIGN_IN|janedoe
iwhygsi|WHOAMI
ykkngzx|CREATE_DISCUSSION|iofetzv.0s|Hey, folks.
sqahhfj|LIST_DISCUSSIONS
ikghbgc|CREATE_DISCUSSION|jpmheij.0s|I love this video. What did you use to make it?
sqahhfj|CREATE_REPLY|t2spqr3|I think it's great
```

## Requirements

- Python 3.11 or higher

## Installation

1. Clone the repository
2. Install the package in development mode:
```bash
pip install -e ".[dev]"
```

## Usage

Run mongodb:
```bash
docker compose up -d
```

Run the server:
```bash
python -m server
```

The server will start listening on port 8989 by default. You can test it using netcat:
```bash
nc -v localhost 8989
```

Type one of the commands (can be found at the beginning of this README) and press enter

## Development

### Running Tests

```bash
pytest
```

### Code Quality

The project uses several tools to ensure code quality:

- Black for code formatting:
```bash
black server tests
```

- Ruff for linting:
```bash
ruff check .
```

- Mypy for type checking:
```bash
mypy server tests
```

## License

MIT 