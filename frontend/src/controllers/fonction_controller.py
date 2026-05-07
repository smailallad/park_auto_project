class FonctionController:
    def __init__(self, fonction_service):
        self.fonction_service = fonction_service

    async def get_fonctions(self):
        return await self.fonction_service.get_all_fonctions()

    async def get_fonction_by_id(self, id):
        return await self.fonction_service.get_fonction_by_id(id)

    async def create_fonction(self, data):
        return await self.fonction_service.create_fonction(data)

    async def update_fonction(self, id, data):
        return await self.fonction_service.update_fonction(id, data)

    async def delete_fonction(self, id):
        return await self.fonction_service.delete_fonction(id)