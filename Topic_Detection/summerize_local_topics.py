import csv


def add_users_topic_to_summary(topics_list, out_dc):
    for topic in topics_list:
        topic = topic.strip()
        if topic in out_dc:
            out_dc[topic] = out_dc[topic] + 1
        else:
            out_dc[topic] = 1
    return out_dc


def save_summary(des, out_dc):
    with open(des, 'w', newline="") as csv_file:
        writer = csv.writer(csv_file)
        for key, value in out_dc.items():
            if value > 1:
                writer.writerow([key, value])


class summarize_local_topics:
    def __init__(self, source_dir, des_file):
        self.source_dir = source_dir
        self.des_file = des_file

    def summarize_user_topics(self):
        out_dc = {}
        processed = 0
        with open(self.source_dir) as sf:
            for line in sf:
                processed += 1
                print(processed)

                topics = str(line).split(':')[1]
                add_users_topic_to_summary(str(topics).split(','),out_dc)
        save_summary(self.des_file, out_dc)
