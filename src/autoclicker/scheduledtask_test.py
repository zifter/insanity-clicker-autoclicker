from datetime import timedelta

from autoclicker.scheduledtask import ScheduledTask


def test_str_ok():
    async def func_test():
        return None

    task = ScheduledTask(timedelta(seconds=5), func_test)

    n = str(task)
    assert n.startswith('func_test at') is True
