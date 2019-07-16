class Institution:

    def __init__(self, data_obj):
        self.pub_ukprn_name = data_obj.get('pub_ukprn_name')
        self.pub_ukprn = data_obj.get('pub_ukprn')
        self.ukprn_name = data_obj.get('ukprn_name')
        self.ukprn = data_obj.get('ukprn')
