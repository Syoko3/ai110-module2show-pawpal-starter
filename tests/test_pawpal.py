import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pawpal_system import Priority, Task, Pet


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_task():
    """A reusable incomplete task for each test."""
    return Task(
        task_id="T1",
        title="Feed the dog",
        description="Morning feeding",
        duration=10,
        priority=Priority.HIGH,
        frequency="daily",
        preferred_time="morning",
    )

@pytest.fixture
def sample_pet():
    """A reusable pet with no tasks attached."""
    return Pet(
        pet_id="P1",
        name="Buddy",
        species="Canine",
        breed="Labrador",
        age=5,
    )


# ---------------------------------------------------------------------------
# Test 1 — Task Completion
# ---------------------------------------------------------------------------

def test_mark_complete_sets_flag(sample_task):
    """mark_complete() should flip is_completed from False to True."""
    assert sample_task.is_completed is False   # pre-condition
    sample_task.mark_complete()
    assert sample_task.is_completed is True    # post-condition


# ---------------------------------------------------------------------------
# Test 2 — Task Addition
# ---------------------------------------------------------------------------

def test_add_task_increases_pet_task_count(sample_pet, sample_task):
    """Adding a task to a pet should increase its task list length by 1."""
    before = len(sample_pet.tasks)
    sample_pet.add_task(sample_task)
    assert len(sample_pet.tasks) == before + 1