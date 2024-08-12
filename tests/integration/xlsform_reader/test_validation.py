import tempfile

import openpyxl
import pytest

from safely_report.survey.xlsform_reader import XLSFormReader


@pytest.mark.parametrize(
    "case_name, error_message",
    [
        ("unsupported_question", "Unsupported question type: geopoint"),
        ("infinite_repeat", "Infinite repeat not allowed: holiday_loop"),
        ("nested_repeat", "Nested repeat not allowed: person_loop"),
        ("unsupported_function", "Unsupported XLSForm function: "
                                 "notyetimplemented"),
    ],
)
def test_xlsform_validation(
    # Fixture(s)
    path_to_xlsform_test_cases,
    # Parameter(s)
    case_name,
    error_message,
):
    with tempfile.NamedTemporaryFile(suffix=".xlsx") as temp_file:
        workbook = openpyxl.load_workbook(path_to_xlsform_test_cases)
        sheet = workbook[case_name]
        sheet.title = "survey"
        workbook.save(temp_file.name)

        with pytest.raises(Exception) as e:
            XLSFormReader.read_xlsform(temp_file.name)
        assert str(e.value) == error_message
