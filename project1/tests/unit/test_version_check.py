import re
import datetime as dt
from typing import Tuple

from version import __version__

# matches version and date from: ## 3.2.0 (2021-07-14)
CHANGELOG_EXP = re.compile(r"^## (\d+.\d+.\d+).*\((\d+-\d+-\d+)\)")


def get_changelog_version_date() -> Tuple[str, str]:
    """
    returns string value of version, date from change log
    """
    with open("CHANGELOG.md", "r") as file:
        for line in file.readlines():
            result = CHANGELOG_EXP.match(line)
            if result is not None:
                return result.groups()

    return None, None


def test_version_incremented():
    ver_str, date_str = get_changelog_version_date()
    assert ver_str is not None, "failed to parse version from changelog"
    assert date_str is not None, "failed to parse date from changelog"
    assert (
        ver_str == __version__
    ), "version file not incremented or not annotated in changelog"
    now = dt.date.today()
    version_date = dt.date.fromisoformat(date_str)
    diff_in_days = (version_date - now).days
    assert diff_in_days < 14, "changelog version seems old. was version updated?"
