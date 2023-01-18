import pipes

from dictionaries import general, jobs, statistics, unavailable

if __name__ == "__main__":
    general_keys = list(general.DICT.keys())
    jobs_keys = list(jobs.JOBS.keys())
    stats_keys = list(statistics.STATISTICS.keys())
    unavail_keys = list(unavailable.UNAVAILABLE.keys())
    all_keys = general_keys + jobs_keys + stats_keys + unavail_keys
    all_dicts = dict(**statistics.STATISTICS, **general.DICT, **jobs.JOBS, **unavailable.UNAVAILABLE)

    with open("en.po", "a") as myfile:
        for key in all_keys:
            text = all_dicts.get(key).get("en") if all_dicts.get(key).get("en") else all_dicts[key]
            br = "\n\n"
            myfile.write(br)
            msgid = "msgid \"{}\"".format(key)
            myfile.write(msgid)
            br = "\n"
            myfile.write(br)
            try:
                msgstr ="msgstr \"{}\"".format(text.replace('"', '\\"'))
            except:
                print(text, key)
            myfile.write(msgstr)

    with open("cy.po", "a") as myfile:
        for key in all_keys:
            text = all_dicts.get(key).get("cy") if all_dicts.get(key).get("cy") else all_dicts[key]
            br = "\n\n"
            myfile.write(br)
            msgid = "msgid \"{}\"".format(key)
            myfile.write(msgid)
            br = "\n"
            myfile.write(br)
            try:
                msgstr = "msgstr \"{}\"".format(text.replace('"', '\\"'))
            except:
                print(text, key)
            myfile.write(msgstr)

    print(len(all_dicts), len(all_keys))
