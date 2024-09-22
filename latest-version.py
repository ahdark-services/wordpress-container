import subprocess
import requests
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Any, List, Optional


@dataclass_json
@dataclass
class Packages:
    full: str
    no_content: Optional[str]
    new_bundled: Optional[str]
    partial: Optional[bool]
    rollback: Optional[bool]


@dataclass_json
@dataclass
class Offer:
    response: str
    download: str
    locale: str
    packages: Packages
    current: str
    version: str
    php_version: str
    mysql_version: str
    new_bundled: Optional[str]
    partial_version: Optional[bool]
    new_files: Optional[bool] = None


@dataclass_json
@dataclass
class WordPressVersionCheck:
    offers: List[Offer]
    translations: List[Any]


def get_latest_version():
    url = "https://api.wordpress.org/core/version-check/1.7/"
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    data = response.json()

    # Deserialize JSON data directly into WordPressVersionCheck object
    version_info = WordPressVersionCheck.from_dict(data)

    # Print out the latest version information
    latest_offer = version_info.offers[0]

    return latest_offer.version


def compare_current_version(latest_version):
    # Compare the current version with the latest version
    with open(".current-version", "r+") as file:
        content = file.read()

        if content != latest_version:
            # Write the latest version to the file
            file.truncate(0)
            file.seek(0)
            file.write(latest_version)

            return True
        else:
            return False


def git_commit(version):
    # Add changes to the staging area
    subprocess.run(
        ["git", "add", ".current-version"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Commit the changes with the provided commit message
    subprocess.run(
        ["git", "commit", "-m", f"Update WordPress to version {version}"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


if __name__ == "__main__":
    version = get_latest_version()
    is_update = compare_current_version(version)
    if is_update:
        git_commit(version)

    print(f"version={version}\nis_update={is_update}")
