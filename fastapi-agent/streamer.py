from pydantic import BaseModel
from core.error_processsor import error_processor
from core.output_processor import output_processor
from core.step_executor import step_executor
from core.query_planner import query_planner
from core.step_maker import step_maker
from core.table_finder.table_selector_from_query import table_selector_from_query
from core.bouncer import bouncer
from core.table_column_name_finder import table_column_name_finder
from core.graph_maker.bar_chart_maker import bar_chart_maker
from core.graph_maker.chart_maker import chart_maker
from utils.logging_config import get_app_logger
from pydantic import BaseModel
import asyncio
from db_factory.db_interface import DatabaseInterface


class QueryRequest(BaseModel):
    query: str

async def streamer(request: QueryRequest, db_instance: DatabaseInterface):
    
    total_tokens = 0
    
    logger = get_app_logger()    
    logger.info(f"Received query: {request.query}")    
    
    yield "<<GGWWP>>$QUERY RECEIVED"
    
    yield "<<GGWWP>>$DOING SAFETY CHECK... "
    
    safe_check, safe_check_tokens = bouncer(request.query)
    total_tokens += safe_check_tokens
    
    if safe_check.isSafe == False:                
        
        reason = str(safe_check.reasoningForSafetyOrDanger)
        
        yield "<<GGWWP>>$QUERY IS NOT SAFE<<GGWWP>>$" + reason
        
        yield "<<GGWWP>>$TOTAL TOKENS USED: " + str(total_tokens)
        
        await asyncio.sleep(2)        
        
        yield "COMPLETED _ END OF STREAM _ FINAL RESULT"
        
        
        return
    
    yield "<<GGWWP>>$CALLING TABLE SELECTOR AGENT"
    
    # table selector: query -> tables
    selected_tables, selected_tables_token = table_selector_from_query(request.query)
    
    total_tokens += selected_tables_token
            
    yield "<<GGWWP>>$Selected Tables are: " + str(selected_tables)
    
    logger.info(f"Calling Query Planner agent")
    
    yield "<<GGWWP>>$CALLING QUERY PLANNER AGENT"
    
    # planner: query -> plan
    plan, plan_token = query_planner(request.query, selected_tables)
    
    total_tokens += plan_token
        
    yield "<<GGWWP>>$Created Plan is : " + str(plan.model_dump_json())
    
    
    yield "<<GGWWP>>$CALLING STEP MAKER AGENT"
    logger.info(f"Calling Step Maker agent")
    
    # step maker: plan -> steps
    steps, steps_token = step_maker(request.query, plan, selected_tables, db_instance)
    
    total_tokens += steps_token
    
    yield "<<GGWWP>>$Created Steps are : " + str(steps.model_dump_json())
    
    yield "<<GGWWP>>$CALLING STEP EXECUTOR AGENT"
    
    logger.info(f"Calling Step Executor agent")
    
    # executor: steps -> results
    query_result, query_result_token = await step_executor(request.query, steps, plan, selected_tables, db_instance)
    
    total_tokens += query_result_token
        
    query_result_str = str(query_result)
    if query_result_str.startswith("Error"):
        logger.error(f"Error in query execution: {query_result}")
        yield "<<GGWWP>>$ERROR IN QUERY EXECUTION - CALLING ERROR PROCESSOR AGENT"
        error_explaination, error_processor_token = error_processor(request.query, query_result_str, steps.steps[len(steps.steps) - 1].sql_query)        
        total_tokens += error_processor_token
        # response = {
        #     "result": error_explaination,    
        #     "error": query_result_str,   
        #     "steps": convert_to_serializable(steps),
        #     "plan": convert_to_serializable(plan)
        # }      
        yield "<<GGWWP>>$ERROR REASON: " + str(error_explaination)
        
        usd_bill = total_tokens * 0.004 / 1000
        bdt_bill = usd_bill * 120
        yield "<<GGWWP>>$TOTAL BILL: USD " + str(usd_bill) + " BDT " + str(bdt_bill)    
        
        yield "<<GGWWP>>$TOTAL TOKENS USED: " + str(total_tokens)
        
        await asyncio.sleep(3)
        
        yield "COMPLETED _ END OF STREAM _ FINAL RESULT"
        
        return
        
        # return str(response)
        
    
    yield "<<GGWWP>>$QUERY EXECUTED SUCCESSFULLY"
    
    column_names, column_names_token = await table_column_name_finder(request.query, steps)   
    print(column_names) 
    total_tokens += column_names_token
    
    # column_names_str = str(column_names)[:-1]
    # column_names_str = column_names_str[:1] + "(" + column_names_str[1:] + ")"
    
    # processed_query_result = column_names_str + str(query_result)
    
    # Combine column names and query result into a formatted string
    # The result will be in the format: [(column1, column2, ...), (row1_data), (row2_data), ...]
    processed_query_result = f"[({', '.join(column_names)}),{str(query_result)[1:]}"
    
    # if queary_result is more than 5000 make it 5000
    trimmed_query_result = query_result
    
    if len(query_result) > 5000:
        # Trim the query result to 5000 characters if it's longer than 5000
        trimmed_query_result = query_result[:5000] if len(query_result) > 5000 else query_result
    
    yield "<<GGWWP>>$Query Result: " + processed_query_result
    
    yield "<<GGWWP>>$ANALYZING IF CHART CAN BE MADE"
    
    chart_config, chart_config_token = await chart_maker(request.query, steps.steps[len(steps.steps) - 1].sql_query, str(trimmed_query_result))
    
    total_tokens += chart_config_token
    
    if chart_config.isBarChartPossible:        
        yield "<<GGWWP>>$CALLING BAR CHART MAKER AGENT"
        
        logger.info(f"Calling Bar Chart Maker agent")
        
        # bar chart: query result -> bar chart        
        
        bar_chart, bar_chart_token = await bar_chart_maker(request.query, str(trimmed_query_result))
        total_tokens += bar_chart_token
        
        # print("bar chart: ",bar_chart)
        
        yield "<<GGWWP>>$Bar Chart is: " + bar_chart    
    
    yield "<<GGWWP>>$CALLING OUTPUT PROCESSOR AGENT"
    
    logger.info(f"Calling Output Processor agent")    
    
    # results -> llm response
    processed_output, processed_output_token = output_processor(request.query, trimmed_query_result)
    
    total_tokens += processed_output_token
    
    yield "<<GGWWP>>$Output Processed: " + str(processed_output)
        
    logger.info(f">>>>>>> Output Processor agent completed-----------------------------------")
    logger.info(f"Result: {processed_output}")
    logger.info(f"Query Result: {query_result}")
    logger.info(f"Steps: {steps}")
    logger.info(f"Plan: {plan}")  
    
    # response = {
    #     "result": processed_output,    
    #     "QueryResult": query_result_str,   
    #     "steps": convert_to_serializable(steps),
    #     "plan": convert_to_serializable(plan)
    # }  
    
    usd_bill = total_tokens * 0.0003 / 1000
    bdt_bill = usd_bill * 120
    yield "<<GGWWP>>$TOTAL BILL: USD " + str(usd_bill) + " BDT " + str(bdt_bill)    
    
    yield "<<GGWWP>>$TOTAL TOKENS USED: " + str(total_tokens)
    
    await asyncio.sleep(3)
    
    yield "COMPLETED _ END OF STREAM _ FINAL RESULT"
    
    # return response
