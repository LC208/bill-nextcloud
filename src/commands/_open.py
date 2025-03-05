from utils.api import NextCloudAPI


def open(item: int, running_operation: int) -> None:
    api = NextCloudAPI.from_item(item)
