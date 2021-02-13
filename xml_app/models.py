from djongo import models

# Create your models here.

class XmlData(models.Model):
    id = models.ObjectIdField()
    xml_attributes = models.JSONField()

