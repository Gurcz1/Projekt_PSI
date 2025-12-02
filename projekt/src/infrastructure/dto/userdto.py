"""A module containing user DTO model."""


from pydantic import UUID4, BaseModel, ConfigDict


class UserDTO(BaseModel):
    """A DTO model for user."""

    id: int
    email: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )