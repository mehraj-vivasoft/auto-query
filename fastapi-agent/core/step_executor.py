from core.query_fixer import query_fixer
from core.query_planner import PlanList
from core.step_maker import QuerySteps
from db_factory.db_interface import DatabaseInterface
from utils.logging_config import get_app_logger, get_db_logger

logger = get_db_logger()

async def step_executor(query: str, queryList: QuerySteps, planList: PlanList, selected_tables: list[str], db_instance: DatabaseInterface):

    number_of_steps = len(queryList.steps)        

    try: 
        logger.info(f"Executing query : {queryList.steps[number_of_steps - 1].sql_query}")
        results = db_instance.execute_query(
            queryList.steps[number_of_steps - 1].sql_query
        )
        logger.info(f"Query result : {results}")
    except Exception as e:
        logger.error(f"Error in executing query : {e}")
        # regenerate the query
        get_app_logger().info(f"Query Execution failed fixing query : {e}")
        fixed_query, fixed_query_tokens = await query_fixer(query, planList, queryList, str(e), selected_tables, db_instance)
        try:
            logger.info(f"Executing fixed query : {fixed_query}")
            results = db_instance.execute_query(fixed_query)
            logger.info(f"Query result : {results}")
            return results, fixed_query_tokens
        except Exception as e:
            logger.error(f"Error in executing fixed query : {e}")            
            return f"Error in executing fixed query : {e}", fixed_query_tokens

    return results, 0
