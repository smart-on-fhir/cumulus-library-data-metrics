from cumulus_library_data_metrics.q_ref_target_valid import q_ref_target_valid


class Summary(q_ref_target_valid.Builder):
    def add_metric_queries(self) -> None:
        super().add_metric_queries()
        self.make_summary(group_column="target")
