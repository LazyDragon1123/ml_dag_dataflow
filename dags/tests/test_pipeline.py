import pytest
from airflow.models import DagBag


class TestDag:

    @pytest.fixture()
    def dagbag(self):
        return DagBag()

    def test_dag_validation(self, dagbag):
        dag = dagbag.get_dag(dag_id="ml_task")
        assert dagbag.import_errors == {}
        assert dag is not None
        assert dag.catchup is True
        assert dag.doc_md != ""

        tasks = dag.tasks
        task_ids = list(map(lambda task: task.task_id, tasks))
        print(f"tasks: {task_ids}")