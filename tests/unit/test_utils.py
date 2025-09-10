import pytest


def format_title(title: str) -> str:
    if not title or not title.strip():
        raise ValueError("Title cannot be empty")
    return title.strip().title()


def test_format_title():
    assert format_title("hello world") == "Hello World"
    assert format_title("  test  ") == "Test"


def test_format_title_empty():
    with pytest.raises(ValueError):
        format_title("")
    
    with pytest.raises(ValueError):
        format_title("   ")
