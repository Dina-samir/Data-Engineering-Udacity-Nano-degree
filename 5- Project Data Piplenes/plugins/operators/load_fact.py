from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                # define params
                 conn_id = "",
                 table = "",
                 sql = "",        
                 append_only = False,
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        # Map params
        self.conn_id = conn_id
        self.table = table
        self.sql = sql
        self.append_only = append_only


    def execute(self, context):
        self.log.info('loading fact data process is started')
        
        redshift = PostgresHook(postgres_conn_id=self.conn_id)
        
        if not self.append_only:
            self.log.info("Delete {} fact table".format(self.table))
            redshift.run("DELETE FROM {}".format(self.table))  
            
        self.log.info("Insert data from staging tables into {} fact table".format(self.table))
        
        insert_statement = f"INSERT INTO {self.table} \n{self.sql}"
        self.log.info(f"Running sql: \n{insert_statement}")
        redshift.run(insert_statement)
        self.log.info(f"Successfully completed insert into {self.table}")

