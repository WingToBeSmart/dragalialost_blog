from djongo import models

# Create your models here.


def upload_location(instance, filename):
    return "%s/%s" % (instance, filename)


class Skill(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to=upload_location, blank=True, null=True,
                             width_field="width_field", height_field="height_field")
    level_1 = models.CharField(max_length=255, blank=True, null=True)
    level_2 = models.CharField(max_length=255, blank=True, null=True)
    level_3 = models.CharField(max_length=255, blank=True, null=True)
    level_4 = models.CharField(max_length=255, blank=True, null=True)


class Adventurer(models.Model):
    name = models.CharField(unique=True, max_length=255)
    class_name = models.CharField(max_length=10)
    element = models.CharField(max_length=10)
    weapon = models.CharField(max_length=15)
    rarity = models.CharField(max_length=1)
    availability = models.CharField(max_length=20)
    hp = models.CharField(max_length=5)
    Str = models.CharField(max_length=5)
    total_max_hp = models.CharField(max_length=5, blank=True, null=True)
    total_max_str = models.CharField(max_length=5, blank=True, null=True)
    base_min_might = models.CharField(max_length=6, blank=True, null=True)
    base_max_might = models.CharField(max_length=6, blank=True, null=True)
    defense = models.CharField(max_length=5, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    race = models.CharField(max_length=15, blank=True, null=True)
    obtained_form = models.CharField(max_length=50, blank=True, null=True)
    icon = models.ImageField(upload_to=upload_location, blank=True, null=True,
                             width_field="width_field", height_field="height_field")
    image = models.ImageField(upload_to=upload_location, blank=True, null=True,
                              width_field="width_field", height_field="height_field")
    url = models.URLField()
    skill_1 = models.ArrayField(model_container=Skill,)
    skill_2 = models.ArrayField(model_container=Skill,)
    remark = models.CharField(max_length=255, blank=True, null=True)
    remark2 = models.CharField(max_length=255, blank=True, null=True)
    remark3 = models.CharField(max_length=255, blank=True, null=True)
    remark4 = models.CharField(max_length=255, blank=True, null=True)
    remark5 = models.CharField(max_length=255, blank=True, null=True)
    release_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            super().save(*args, **kwargs)
