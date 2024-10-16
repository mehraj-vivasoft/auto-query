from pydantic import BaseModel
from core.query_fixer import query_fixer
from core.query_planner import PlanList
from core.step_maker import QuerySteps
from db.database import execute_query
from utils.logging_config import get_db_logger
    
logger = get_db_logger()    
    
async def step_executor(query: str, queryList: QuerySteps, planList: PlanList):
    
    number_of_steps = len(queryList.steps)
    
    try: 
        results = await execute_query(queryList.steps[number_of_steps - 1].sql_query)
        logger.info(f"Query result : {results}")
    except Exception as e:
        logger.error(f"Error in executing query : {e}")                
        # regenerate the query
        fixed_query = await query_fixer(query, planList, queryList, str(e))
        try:
            results = await execute_query(fixed_query)
            logger.info(f"Query result : {results}")
            return results
        except Exception as e:
            logger.error(f"Error in executing fixed query : {e}")
            return f"Error in executing fixed query : {e}"
            
    return results