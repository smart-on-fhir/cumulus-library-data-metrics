from cumulus_library_data_metrics.q_date_recent import q_date_recent


class Summary(q_date_recent.Builder):
    def add_metric_queries(self) -> None:
        super().add_metric_queries()
        self.make_summary()
