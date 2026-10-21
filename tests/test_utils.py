from src.utils import read_json_file


def test_read_json_file():
    result = read_json_file("data/operations.json")

    assert isinstance(result, list)


def test_read_json_file_empty(tmp_path):
    file_path = tmp_path / "empty.json"
    file_path.write_text("")

    result = read_json_file(file_path)

    assert result == []


def test_read_json_file_not_list(tmp_path):
    file_path = tmp_path / "data.json"
    file_path.write_text('{"name": "Maria"}')

    result = read_json_file(file_path)

    assert result == []


def test_read_json_file_not_found():
    result = read_json_file("data/does_not_exist.json")

    assert result == []
