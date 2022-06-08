from typing import List
import pytest

from ..app import app, client
from ..models.groups import GroupDetailed


class TestGroups:
    # @pytest.mark.get_groups
    def test_route_exist(self) -> None:
        res = client.get(
            app.url_path_for('get groups'),
            json={},
        )
        assert res.status_code == 200

    # @pytest.mark.get_groups
    def test_invalid_ouput_raise_error(self) -> None:
        res = client.get(
            app.url_path_for("get groups"),
        )
        assert res.json() == List[GroupDetailed]
