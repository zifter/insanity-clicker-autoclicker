from insanity_clicker.stats import AppStats


def test_print_stats():
    stat = AppStats()

    view = str(stat)
    print(view)
    assert view != ''


def test_sum_stats_ok():
    stat = AppStats()

    stat.click()
    stat.click()
    stat.amnesia()

    stat.click()
    stat.hire()

    total = stat.total_run_stats()
    assert total.clicks == 3
    assert total.hired == 1
