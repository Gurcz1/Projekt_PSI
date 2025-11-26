"""A repository for user entity."""

from abc import ABC, abstractmethod 

from pydantic import UUID1

from src.core.domain.user import UserIn, User


class IUserRepository(ABC):
    """An abstract repository class for user."""

    @abstractmethod
    async def register_user(self, user: UserIn) -> User | None:
        """A method registering new user.

        Args:
            user (UserIn): The user input data.

        Returns:
            Any | None: The new user object.
        """
    @abstractmethod
    async def get_by_uuid(self, uuid: UUID1) -> User | None:
        """A method getting user by UUID.

        Args:
            uuid (UUID5): UUID of the user.

        Returns:
            Any | None: The user object if exists.
        """

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        """A method getting user by email.

        Args:
            email (str): The email of the user.

        Returns:
            Any | None: The user object if exists.
        """