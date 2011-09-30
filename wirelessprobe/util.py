def avg(log):
    return sum(log) / len(log)

def make_stats(log):
    if log:
        return dict(min=min(log), max=max(log), avg=avg(log))
    else:
        return dict(min=None, max=None, avg=None)

