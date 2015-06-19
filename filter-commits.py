import re
import sys

def get_shortlog(filename):
    shortlog = dict()

    for line in open(filename).readlines():
        line = line.strip()
        if line == '':
            continue

        # This breaks for authors with different name than first-last..
        m = re.match(r"(?P<name>\S+ \S+) \((?P<commits>\d+)\)\:", line)
        if m:
            author = "%s" % m.group('name')
            shortlog[author] = []
            continue

        shortlog[author].append(line)

    return shortlog

# Assumes new is a superset of old..
def diff_shortlog(old_log, new_log):
    diff_log = dict()

    for author in new_log.keys():
        new_commits = new_log[author]

        try:
            old_commits = old_log[author]
        except KeyError:
            diff_log[author] = new_commits
            continue

        only_new = [ c for c in new_log[author] if c not in old_log[author] ]
        if len(only_new) > 0:
            diff_log[author] = only_new

    return diff_log

def print_shortlog(shortlog):
    for author in sorted(shortlog.keys()):
        commits = shortlog[author]
        num_commits = len(commits)

        print "%s (%d):" % (author, num_commits)
        for commit in commits:
            print "      %s" % commit
        print ""

def main(old, new=None):
    old_log = get_shortlog(old)
    new_log = get_shortlog(new)

    diff_log = diff_shortlog(old_log, new_log)
    print_shortlog(diff_log)

if __name__ == "__main__":
    try:
        old_log = sys.argv[1]
        new_log = sys.argv[2]
    except KeyError:
        print "Usage: %s: old_shortlog new_shortlog" % (sys.argv[0])

    main(old_log, new_log)
