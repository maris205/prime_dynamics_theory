from experiments import build_archive


def test_archive_membership_and_status() -> None:
    assert len(build_archive.LOCAL_MEMBERS) == 21
    assert len(build_archive.EXTERNAL_INPUTS) == 9
    assert all(".." not in member.split("/") for member in build_archive.LOCAL_MEMBERS)
    assert all(".." not in member.split("/") for member in build_archive.EXTERNAL_INPUTS)
