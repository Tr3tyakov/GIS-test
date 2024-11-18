import asyncio

from app.config import settings
from app.core.context import ApplicationContext
from app.core.database import Database
from app.core.enums import CoordinateReferenceSystemEnum
from app.models.coordinate_reference_system import CoordinateReferenceSystem


class CoordinateReferenceSystemSeed:
    """Cид, наполняющий координатные системы в БД"""

    def __init__(self, context: ApplicationContext):
        self.context = context

    async def create_coordinate_reference_systems(self):
        created_instances = []
        for coordinate_system_data in CoordinateReferenceSystemEnum:
            created_instances.append(
                CoordinateReferenceSystem(
                    name=coordinate_system_data.value,
                    srid=coordinate_system_data.srid
                )
            )

        async with self.context.database.session() as session:
            session.add_all(created_instances)


if __name__ == "__main__":
    database = Database(settings=settings.POSTGRES)
    database._connect()

    seed = CoordinateReferenceSystemSeed(context=ApplicationContext(database=database))
    asyncio.run(seed.create_coordinate_reference_systems())
