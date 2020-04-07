from django.db import models
from datetime import datetime
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
# Create your models here.


def upload_icon(instance, filename):
    return "upload/icon/%s" % (filename)


def upload_image(instance, filename):
    return "upload/image/%s" % (filename)


class Skill(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to=upload_icon, blank=True, null=True,)
    icon_url = models.URLField()
    level_1 = models.CharField(max_length=255, blank=True, null=True)
    level_2 = models.CharField(max_length=255, blank=True, null=True)
    level_3 = models.CharField(max_length=255, blank=True, null=True)
    level_4 = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            skill = Skill.objects.get(name=self.name)
            return skill
        except (Skill.DoesNotExist):
            if self.icon_url and not self.icon:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(urlopen(self.icon_url).read())
                img_temp.flush()
                self.icon.save(f"{self.name}.png", File(img_temp))
            super().save(*args, **kwargs)
            return Skill.objects.get(name=self.name)


class Ability(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to=upload_icon, blank=True, null=True,)
    icon_url = models.URLField()
    level = models.CharField(max_length=5, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            ability = Ability.objects.get(name=self.name)
            return ability
        except (Ability.DoesNotExist):
            if self.icon_url and not self.icon:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(urlopen(self.icon_url).read())
                img_temp.flush()
                self.icon.save(f"{self.name}.png", File(img_temp))
            super().save(*args, **kwargs)
            return Ability.objects.get(name=self.name)


class AdventurerAbility(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to=upload_icon, blank=True, null=True,)
    icon_url = models.URLField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            adv_ability = AdventurerAbility.objects.get(name=self.name)
            return adv_ability
        except (AdventurerAbility.DoesNotExist):
            if self.icon_url and not self.icon:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(urlopen(self.icon_url).read())
                img_temp.flush()
                self.icon.save(f"{self.name}.png", File(img_temp))
            super().save(*args, **kwargs)
            return AdventurerAbility.objects.get(name=self.name)


class WeaponAbility(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to=upload_icon, blank=True, null=True,)
    icon_url = models.URLField()
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            weapon_ability = WeaponAbility.objects.get(name=self.name)
            return weapon_ability
        except (WeaponAbility.DoesNotExist):
            if self.icon_url and not self.icon:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(urlopen(self.icon_url).read())
                img_temp.flush()
                self.icon.save(f"{self.name}.png", File(img_temp))
            super().save(*args, **kwargs)
            return WeaponAbility.objects.get(name=self.name)


class Adventurer(models.Model):
    name = models.CharField(unique=True, max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
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
    icon = models.ImageField(upload_to=upload_icon, blank=True, null=True,)
    icon_url = models.URLField()
    image = models.ImageField(
        upload_to=upload_image, blank=True, null=True,)
    image_url = models.URLField()
    url = models.URLField()
    skill_1 = models.ForeignKey(
        Skill, on_delete=models.CASCADE, related_name='skill_1', blank=True, null=True,)
    skill_2 = models.ForeignKey(
        Skill, on_delete=models.CASCADE, related_name='skill_2', blank=True, null=True,)
    co_ability = models.ForeignKey(
        AdventurerAbility, on_delete=models.CASCADE, related_name='co_ability', blank=True, null=True,)
    chain_co_ability = models.ForeignKey(
        AdventurerAbility, on_delete=models.CASCADE, related_name='chain_co_ability', blank=True, null=True,)
    ability_1 = models.ForeignKey(
        AdventurerAbility, on_delete=models.CASCADE, related_name='ability_1', blank=True, null=True,)
    ability_2 = models.ForeignKey(
        AdventurerAbility, on_delete=models.CASCADE, related_name='ability_2', blank=True, null=True,)
    ability_3 = models.ForeignKey(
        AdventurerAbility, on_delete=models.CASCADE, related_name='ability_3', blank=True, null=True,)
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
        try:
            adv = Adventurer.objects.get(name=self.name)
            return None
        except (Adventurer.DoesNotExist):
            if self.icon_url and not self.icon:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(urlopen(self.icon_url).read())
                img_temp.flush()
                self.icon.save(f"{self.name}.png", File(img_temp))
            super(Adventurer, self).save(*args, **kwargs)
            return Adventurer.objects.get(name=self.name)


class Dragon(models.Model):
    name = models.CharField(unique=True, max_length=255)
    element = models.CharField(max_length=10)
    rarity = models.CharField(max_length=1)
    availability = models.CharField(max_length=20)
    group = models.CharField(max_length=20, blank=True, null=True)
    hp = models.CharField(max_length=5)
    Str = models.CharField(max_length=5)
    sell_value = models.CharField(max_length=6, blank=True, null=True)
    sell_value_mana = models.CharField(max_length=6, blank=True, null=True)
    base_min_might = models.CharField(max_length=6, blank=True, null=True)
    base_max_might = models.CharField(max_length=6, blank=True, null=True)
    favorite_gift = models.CharField(max_length=30, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    obtained_form = models.CharField(max_length=50, blank=True, null=True)
    icon = models.ImageField(upload_to=upload_icon, blank=True, null=True,)
    icon_url = models.URLField()
    image = models.ImageField(
        upload_to=upload_image, blank=True, null=True,)
    image_url = models.URLField()
    url = models.URLField()
    skill = models.ForeignKey(
        Skill, on_delete=models.CASCADE, related_name='dragon_skill', blank=True, null=True,)
    ability_1 = models.ManyToManyField(
        Ability, related_name='dragon_ability_1', )
    ability_2 = models.ManyToManyField(
        Ability, related_name='dragon_ability_2', )
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
        try:
            adv = Dragon.objects.get(name=self.name)
            return None
        except (Dragon.DoesNotExist):
            if self.icon_url and not self.icon:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(urlopen(self.icon_url).read())
                img_temp.flush()
                self.icon.save(f"{self.name}.png", File(img_temp))
            super(Dragon, self).save(*args, **kwargs)
            return Dragon.objects.get(name=self.name)


class Wyrmprint(models.Model):
    name = models.CharField(unique=True, max_length=255)
    rarity = models.CharField(max_length=1)
    availability = models.CharField(max_length=20)
    hp = models.CharField(max_length=5)
    Str = models.CharField(max_length=5)
    sell_value = models.CharField(max_length=6, blank=True, null=True)
    sell_value_mana = models.CharField(max_length=6, blank=True, null=True)
    base_min_might = models.CharField(max_length=6, blank=True, null=True)
    base_max_might = models.CharField(max_length=6, blank=True, null=True)
    favorite_gift = models.CharField(max_length=30, blank=True, null=True)
    obtained_form = models.CharField(max_length=50, blank=True, null=True)
    icon = models.ImageField(upload_to=upload_icon, blank=True, null=True,)
    icon_url = models.URLField()
    image = models.ImageField(
        upload_to=upload_image, blank=True, null=True,)
    image_url = models.URLField()
    url = models.URLField()
    ability_1 = models.ManyToManyField(
        Ability, related_name='wyrmprint_ability_1', )
    ability_2 = models.ManyToManyField(
        Ability, related_name='wyrmprint_ability_2', )
    ability_3 = models.ManyToManyField(
        Ability, related_name='wyrmprint_ability_3', )
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
        try:
            adv = Wyrmprint.objects.get(name=self.name)
            return None
        except (Wyrmprint.DoesNotExist):
            if self.icon_url and not self.icon:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(urlopen(self.icon_url).read())
                img_temp.flush()
                self.icon.save(f"{self.name}.png", File(img_temp))
            super(Wyrmprint, self).save(*args, **kwargs)
            return Wyrmprint.objects.get(name=self.name)


class Weapon(models.Model):
    name = models.CharField(unique=True, max_length=255)
    rarity = models.CharField(max_length=1)
    element = models.CharField(max_length=10)
    weapon_type = models.CharField(max_length=15)
    availability = models.CharField(max_length=20)
    group = models.CharField(max_length=20, blank=True, null=True)
    hp = models.CharField(max_length=5)
    Str = models.CharField(max_length=5)
    sell_value = models.CharField(max_length=6, blank=True, null=True)
    base_min_might = models.CharField(max_length=6, blank=True, null=True)
    base_max_might = models.CharField(max_length=6, blank=True, null=True)
    favorite_gift = models.CharField(max_length=30, blank=True, null=True)
    obtained_form = models.CharField(max_length=50, blank=True, null=True)
    icon = models.ImageField(upload_to=upload_icon, blank=True, null=True,)
    icon_url = models.URLField()
    image = models.ImageField(
        upload_to=upload_image, blank=True, null=True,)
    image_url = models.URLField()
    url = models.URLField()
    skill = models.ForeignKey(
        Skill, on_delete=models.CASCADE, related_name='weapon_skill', blank=True, null=True,)
    ability_1 = models.ForeignKey(
        WeaponAbility, on_delete=models.CASCADE, related_name='weapon_ability_1', blank=True, null=True,)
    ability_2 = models.ForeignKey(
        WeaponAbility, on_delete=models.CASCADE, related_name='weapon_ability_2', blank=True, null=True,)
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
        try:
            adv = Weapon.objects.get(name=self.name)
            return None
        except (Weapon.DoesNotExist):
            if self.icon_url and not self.icon:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(urlopen(self.icon_url).read())
                img_temp.flush()
                self.icon.save(f"{self.name}.png", File(img_temp))
            super(Weapon, self).save(*args, **kwargs)
            return Weapon.objects.get(name=self.name)


class News(models.Model):
    name = models.CharField(unique=True, max_length=50)
    category = models.CharField(max_length=20)
    content = models.CharField(max_length=255, blank=True, null=True,)
    status = models.IntegerField(default=1)
    image = models.ImageField(
        upload_to=upload_image, blank=True, null=True,)
    image_url = models.URLField()
    url = models.URLField()
    release_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            adv = News.objects.get(name=self.name)
            return None
        except (News.DoesNotExist):
            if self.image_url and not self.image:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(urlopen(self.image_url).read())
                img_temp.flush()
                self.image.save(f"{self.name}.png", File(img_temp))
            super(News, self).save(*args, **kwargs)
            return News.objects.get(name=self.name)
