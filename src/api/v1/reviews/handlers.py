from fastapi import APIRouter, HTTPException, Depends, status
from punq import Container

from src.api.v1.dependencies import init_container
from src.api.v1.reviews.schemas import ReviewResponseSchema, ReviewRequestSchema
from src.api.v1.schemas import ErrorSchema
from src.services.mediator import Mediator
from src.utils.exceptions import ApplicationException
from src.utils.logger import logger

router = APIRouter(tags=["Review"])


@router.post(
    "/review",

    description='Endpoint for creating a review',
    responses={
        status.HTTP_200_OK: {'model': ReviewResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
        status.HTTP_429_TOO_MANY_REQUESTS: {'model': ErrorSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': ErrorSchema},
    },
)
async def review_code(
        schema: ReviewRequestSchema,
        container: Container = Depends(init_container),
) -> ReviewResponseSchema:
    mediator = container.resolve(Mediator)

    try:
        logger.info(f"Starting review generation for repo: {schema.github_repo_url}")
        result = await mediator.generate_review(
            schema.github_repo_url,
            schema.assignment_description,
            schema.candidate_level
        )
        logger.info(f"Review generated successfully for {schema.github_repo_url}")
    except ApplicationException as e:
        logger.error(f"Error processing code review request for {schema.github_repo_url}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return ReviewResponseSchema.from_dict(result)
