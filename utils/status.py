def update_status(status: str):
    with open('status.txt', 'w') as f:
        f.write(status)


def read_status() -> str:
    with open('status.txt', 'r') as f:
        return f.readline()