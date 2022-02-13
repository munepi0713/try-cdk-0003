
def handler(event, context):
    '''Echo input twice.'''
    print(event)
    print(context)

    # This return data is similar to one for API Gateway integration, 
    # though no format regulation about a return value from Lambda handler
    # for StepFunction integration.
    return { 
        'statusCode': 200,
        'message' : [event, event]
    }
