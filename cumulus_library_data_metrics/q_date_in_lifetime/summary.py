from cumulus_library_data_metrics.q_date_in_lifetime import q_date_in_lifetime


class Summary(q_date_in_lifetime.Builder):
    def add_metric_queries(self) -> None:
        super().add_metric_queries()
        self.make_summary()
