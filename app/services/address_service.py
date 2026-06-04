from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.address_repo import AddressRepository
from app.schemas.address import (
    AddressResponse,
)

address_repo = AddressRepository()


class AddressService:
    def _dt(self, value: datetime | None) -> datetime:
        return value or datetime.now(timezone.utc)

    def _to_response(self, item) -> AddressResponse:
        return AddressResponse(
            id=item.id,
            title=item.title,
            phone=item.phone,
            address=item.address,
            status=item.status,
            created_date=self._dt(item.created_date),
            modified_date=self._dt(item.modified_date),
        )

    async def get_addresses(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> list[AddressResponse]:
        items = await address_repo.list_by_user(
            db,
            user_id,
        )

        return [
            self._to_response(item)
            for item in items
        ]

    async def create_address(
        self,
        db: AsyncSession,
        user_id: int,
        body,
    ) -> AddressResponse:
        item = await address_repo.create(
            db,
            user_id,
            body.title,
            body.phone,
            body.address,
            body.status,
        )

        return self._to_response(item)

    async def update_address(
        self,
        db: AsyncSession,
        user_id: int,
        address_id: int,
        body,
    ) -> AddressResponse:
        item = await address_repo.get_by_id_for_user(
            db,
            address_id,
            user_id,
        )

        if not item:
            raise ValueError("Address not found")

        item = await address_repo.update(
            db,
            item,
            body.title,
            body.phone,
            body.address,
            body.status,
        )

        return self._to_response(item)

    async def delete_address(
        self,
        db: AsyncSession,
        user_id: int,
        address_id: int,
    ) -> None:
        item = await address_repo.get_by_id_for_user(
            db,
            address_id,
            user_id,
        )

        if not item:
            raise ValueError("Address not found")

        await address_repo.delete(
            db,
            item,
        )