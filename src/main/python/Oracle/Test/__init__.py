class Adaptee:
    def save_json(self):
        self.filename = 'agg_data_{}.json'.format(datetime.date(datetime.now()))
        self.df.astype(str).to_json(os.path.join(save_dir, self.filename))
        print('...', self.filename)

class Adapter(AggReport, Adaptee):
    def save_csv(self):
        self.save_json()

aggReportJsonAdapter = Adapter(df=df)
aggReportJsonAdapter.save_csv()