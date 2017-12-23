import uuid
from django.db import models


class AbstractUUID(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, db_index=True)

    def uuid_str(self):
        return str(self.uuid)

    class Meta:
        abstract = True
