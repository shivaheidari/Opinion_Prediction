import sys
import meaningcloud
import Utils


def write_header_to_file(file_path, header):
    with open(file_path, 'a+') as uf:
        uf.write(header + '\n')


def get_category_and_terms_from_response(entities, topics_response):
    for entity in entities:
        res = topics_response.getCategories()
        for j in range(0, len(res)):
            topic_str = res[j]['label']
            terms = []
            if 'term_list' in res[0]:
                for tr in (res[j]['term_list']):
                    terms = tr['form']
        return topic_str, terms


class meaning_cloud_topic_detection:
    def __init__(self, model, license_key, source_file, des_file):
        self.model = model
        self.license_key = license_key
        self.source_file = source_file
        self.des_file = des_file

    def call_meaning_cloud(self):

        write_header_to_file(self.des_file, 'term;topic;words')

        topic_words = Utils.Utils().csv_read(self.source_file)
        t_processed = 0

        for item in topic_words:
            tweet_text = item[0].strip()
            t_processed += 1
            print(t_processed)
            try:
                topics_response = meaningcloud.DeepCategorizationResponse(
                    meaningcloud.DeepCategorizationRequest(self.license_key, txt=tweet_text, model=self.model,
                                                           otherparams={'verbose': 'y'}).sendReq())
                if topics_response.isSuccessful():
                    entities = topics_response.getCategories()
                    if entities:
                        topic_str, terms = get_category_and_terms_from_response(entities, topics_response)
                        with open(self.des_file, 'a+') as uf:
                            #uf.write(tweet_text + ";" + topic_str + "," + ' '.join(terms) + "\n")
                            uf.write(tweet_text + ";" + topic_str + "\n")
                    else:
                        print("\nOh no! There was the following error: " + topics_response.getStatusMsg() + "\n")
                else:
                    if topics_response.getResponse() is None:
                        print("\nOh no! The request sent did not return a Json\n")
                    else:
                        print("\nOh no! There was the following error: " + topics_response.getStatusMsg() + "\n")

            except ValueError:
                e = sys.exc_info()[0]
                print("\nException: " + str(e))
