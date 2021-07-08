from model_utils.models import TimeStampedModel
from safedelete.models import SafeDeleteModel

class BaseModel(TimeStampedModel, SafeDeleteModel):

    class Meta:
        abstract = True