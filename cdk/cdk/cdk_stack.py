from aws_cdk import (
    Duration,
    aws_lambda as lambda_,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
    Stack,
    CfnOutput,
    # aws_sqs as sqs,
)
from constructs import Construct

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        async_task_function = lambda_.Function(
            self,
            "EchoTwiceFunction",
            # code=lambda_.Code.from_docker_build(path="../async-task/src"),
            code=lambda_.Code.from_asset_image(directory="../async-task/src"),
            runtime=lambda_.Runtime.FROM_IMAGE,
            handler=lambda_.Handler.FROM_IMAGE,
            timeout=Duration.seconds(25),
        )

        state_machine = sfn.StateMachine(
            self,
            "EchoTwiceStateMachine",
            definition=tasks.LambdaInvoke(
                self, "EchoTwiceTask", lambda_function=async_task_function
            ).next(sfn.Succeed(self, "Success")),
        )

        # Output state machine's ARN.
        CfnOutput(
            self,
            "EchoTwiceStateMachineArn",
            value=state_machine.state_machine_arn,
            export_name="C0003:EchoTwiceStateMachineArn",
        )
