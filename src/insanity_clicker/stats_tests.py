from insanity_clicker.stats import AppStats


def test_print_stats():
    stat = AppStats()

    view = str(stat)
    print(view)
    assert view != ''
