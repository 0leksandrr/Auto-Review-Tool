from fastapi import APIRouter, status, Depends, HTTPException
from punq import Container

from src.api.v1.assistant.schemas import AssistantSchemaResponse, AssistantSchemaRequest
from src.api.v1.dependencies import init_container
from src.api.v1.schemas import ErrorSchema
from src.services.commands.assistant import AssistCommand
from src.services.mediator import Mediator
from src.utils.exceptions import ApplicationException
from src.utils.logger import logger

router = APIRouter(tags=["AI Assistant"])


@router.post(
    "/assist",
    description="Endpoint with AI assistant. Accepts customer requests with product links and descriptions.",
    responses={
        status.HTTP_200_OK: {'model': AssistantSchemaResponse},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
        status.HTTP_429_TOO_MANY_REQUESTS: {'model': ErrorSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': ErrorSchema},
    },
)
async def assist(
        schema: AssistantSchemaRequest,
        container: Container = Depends(init_container),
) -> AssistantSchemaResponse:
    mediator = container.resolve(Mediator) 

    try:
        result = await mediator.handle_command(AssistCommand(
            description=schema.description,
            links=schema.links
            )
        )
    except ApplicationException as e:
        logger.error(f"Error : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return AssistantSchemaResponse.create(result)
