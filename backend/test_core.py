import pytest
from core import calculate_score

def test_no_issues_gives_perfect_score():
    score, grade = calculate_score([])
    assert score == 10.0
    assert grade == "A"

def test_single_minor_issue():
    issues = [{"severity": "minor"}]
    score, grade = calculate_score(issues)
    assert score == 9.5
    assert grade == "A"

def test_single_major_issue():
    issues = [{"severity": "major"}]
    score, grade = calculate_score(issues)
    assert score == 8.5
    assert grade == "B"

def test_single_critical_issue():
    issues = [{"severity": "critical"}]
    score, grade = calculate_score(issues)
    assert score == 7.0
    assert grade == "B"

def test_multiple_critical_issues_cap_at_zero():
    issues = [{"severity": "critical"}] * 5
    score, grade = calculate_score(issues)
    assert score == 0
    assert grade == "F"

def test_mixed_severity_issues():
    issues = [
        {"severity": "critical"},
        {"severity": "major"},
        {"severity": "minor"},
    ]
    score, grade = calculate_score(issues)
    assert score == 5.0
    assert grade == "C"

def test_grade_boundaries():
    assert calculate_score([{"severity": "minor"}])[1] == "A"
    assert calculate_score([{"severity": "critical"}])[1] == "B"
    assert calculate_score([{"severity": "critical"}, {"severity": "critical"}])[1] == "D"
