import traceback
import json

from pytest import mark

SOURCE_DOC = "docs/use_cases.adoc"


@mark.docs
def test_single_value_string(load_doc):
    expected, console = load_doc(SOURCE_DOC)
    assert console.exit_code == 0, "Command should complete successfully"
    assert len(expected) == 12, "Console output from doc should be 10 characters long (plus quotes)"
    assert 10 <= len(console.output.strip()) <= 12, "Length of string should be 8 - 10 chars long (plus quotes)"


@mark.docs
def test_single_value_integer(load_doc):
    expected, console = load_doc(SOURCE_DOC)
    assert console.exit_code == 0, f"Command Errored: {console.exception}"
    int(expected)
    gen_val = int(console.output)
    assert 5 <= gen_val <= 10, "Generated Integer should be between 5 and 10"


@mark.docs
def test_random_choice(load_doc):
    expected, console = load_doc(SOURCE_DOC)
    assert console.exit_code == 0, "Command should complete successfully"
    assert console.output[:-1] in {'"red"', '"yellow"', '"blue"', '"orange"', '"green"', '"purple"'}, "Choice should be a colour"


@mark.docs
def test_single_value_object(load_doc):
    expected, console = load_doc(SOURCE_DOC)
    if console.exit_code:
        traceback.print_tb(console.exc_info[2])
    assert console.exit_code == 0, f"Command Errored: {console.exception}\n{traceback.print_stack(console.exc_info)}"
    exp_obj = json.loads(expected)
    gen_obj = json.loads(console.output)
    assert (
        isinstance(exp_obj, dict) and isinstance(gen_obj, dict),
        f"Expecting dict but got {type(exp_obj)}/{type(gen_obj)} instead",
    )
    assert len(exp_obj) == 4 and len(gen_obj) == 4, "Each object should have 3 properties"
    assert "field_1" in exp_obj and "field_1" in gen_obj, "'field_1' should be an object in both sets"
    assert isinstance(gen_obj["field_1"], str)
    assert isinstance(gen_obj["field_2"], int)
    assert isinstance(gen_obj["field_3"], float)
    assert gen_obj["field_4"] in {"small", "medium", "large"}


@mark.docs
def test_multi_value_string(load_doc):
    expected, console = load_doc(SOURCE_DOC)
    assert console.exit_code == 0, "Command should complete successfully"
    generated_lines = console.output[:-1].split("\n")
    assert len(generated_lines) == 5, "Should have generated 5 values"
    assert all([8 <= len(line) <= 22 for line in generated_lines])


@mark.docs
def test_static_ref_events(load_doc):
    expected, console = load_doc(SOURCE_DOC)
    assert console.exit_code == 0, "Command should complete successfully"
    generated_lines = [
        json.loads(line) for line in console.output[:-1].split("\n")
    ]
    names = [ev["user_id"] for ev in generated_lines]
    timestamps = [ev["timestamp"] for ev in generated_lines]
    assert len(generated_lines) == 5, "Should have generated 5 values"
    assert all([name == "jdoe" for name in names])
    assert all([timestamps[a - 1] + 5 == timestamps[a] for a in range(1, len(timestamps))])


@mark.docs
def test_static_ref_random_start(load_doc):
    expected, console = load_doc(SOURCE_DOC)
    assert console.exit_code == 0, "Command should complete successfully"
    generated_lines = [
        json.loads(line) for line in console.output[:-1].split("\n")
    ]
    names = [ev["user_id"] for ev in generated_lines]
    timestamps = [ev["timestamp"] for ev in generated_lines]
    assert len(generated_lines) == 5, "Should have generated 5 values"
    assert 3 <= len(names[0]) <= 6
    assert all([name == names[0] for name in names])
    assert all([timestamps[a - 1] + 5 == timestamps[a] for a in range(1, len(timestamps))])


@mark.docs
def test_seq_format_string(load_doc):
    expected, console = load_doc(SOURCE_DOC)
    assert console.exit_code == 0, "Command should complete successfully"
    generated_lines = [
        json.loads(line) for line in console.output[:-1].split("\n")
    ]
    assert all([ev.endswith("-test") for ev in generated_lines])
    assert all([len(ev) == 10 for ev in generated_lines])


@mark.docs
def test_cond_status_change(load_doc):
    expected, console = load_doc(SOURCE_DOC)
    assert console.exit_code == 0, "Command should complete successfully"
    generated_lines = [
        json.loads(line) for line in console.output[:-1].split("\n")
    ]
    print(generated_lines)
    # TODO: Fix Dependency Management
