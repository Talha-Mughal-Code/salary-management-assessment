from app.models import Employee

table = Employee.__table__


def test_every_column_is_required():
    assert [column.name for column in table.columns if column.nullable] == []


def test_email_has_a_unique_index():
    indexes = {index.name: index.unique for index in table.indexes}

    assert indexes["ix_employees_email"] is True


def test_list_filters_are_indexed():
    indexed = {column.name for index in table.indexes for column in index.columns}

    assert {"country", "job_title", "department"} <= indexed


def test_salary_must_be_positive():
    checks = [
        str(constraint.sqltext)
        for constraint in table.constraints
        if constraint.name == "ck_employees_salary_positive"
    ]

    assert checks == ["salary > 0"]
