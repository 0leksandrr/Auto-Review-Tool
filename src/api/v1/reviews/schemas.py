from pydantic import BaseModel


class ReviewRequestSchema(BaseModel):
    assignment_description: str
    github_repo_url: str
    candidate_level: str


class ReviewResponseSchema(BaseModel):
    found_files: list
    downsides_comments: str
    rating: str
    conclusion: str

    @classmethod
    def from_dict(cls, data: dict) -> "ReviewResponseSchema":
        return cls(
            found_files=data.get("found_files", []),
            downsides_comments=data.get("downsides_comments", ""),
            rating=data.get("rating", ""),
            conclusion=data.get("conclusion", "")
        )
