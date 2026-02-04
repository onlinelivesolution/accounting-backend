from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession


class NumericCodeGenerator:
    @staticmethod
    async def get_next_code(
        db: AsyncSession,
        model,
        field,
        length: int
    ) -> str:
        """
        Generate next numeric code with fixed length.
        Example:
            max = 9, length=4  -> '0010'
            max = None         -> '0001'
        """

        result = await db.execute(
            select(func.max(field))
        )
        max_code = result.scalar()

        if max_code is None:
            next_number = 1
        else:
            # Handle varchar numeric safely
            next_number = int(max_code) + 1

        return str(next_number).zfill(length)
