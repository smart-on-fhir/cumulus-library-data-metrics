from cumulus_library_data_metrics.q_system_use import q_system_use


class Summary(q_system_use.Builder):
    def add_metric_queries(self) -> None:
        super().add_metric_queries()
        self.make_summary(group_column="field")
