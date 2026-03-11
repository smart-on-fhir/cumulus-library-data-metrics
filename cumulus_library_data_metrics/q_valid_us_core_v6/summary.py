from cumulus_library_data_metrics.q_valid_us_core_v6 import q_valid_us_core_v6


class Summary(q_valid_us_core_v6.Builder):
    def add_metric_queries(self) -> None:
        super().add_metric_queries()
        self.make_summary(group_column="profile")
