import pytest
from unittest.mock import patch

from core.tests.fixtures import user_bob

@pytest.mark.django_db
@patch("external_apis.mk2.book_seat")
def test_book_movie(mock_book_seat, user_bob):
    # Given
    payload = {
        "theater_id": 1,
        "movie_name": "Big Fight!",
        "date": "2026-12-31 22:00:00",
    }

    mock_book_seat.return_value = {"success": True}

    expected_theater_name = "MK2 Gambetta"

    # When
    response = user_bob.client.post(
        "/core/book_movie/", payload, content_type="application/json",
    )

    # Then
    assert response.status_code == 200
    mock_book_seat.assert_called_once_with(
        theater_name=expected_theater_name,
        movie_name="Big Fight!",
        date="2026-12-31 22:00:00",
    )
