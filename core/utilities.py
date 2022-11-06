import random
import string

from django.utils.text import slugify


def generate_random_string(length):
    return "".join(random.choices(string.ascii_lowercase, k=int(length)))



def generate_unique_slug(instance, base_title, new=False, update=False):
    slug = slugify(base_title)
    model = instance.__class__

    if new:
        slug = new

    if update:
        slug_exists = model.objects.filter(
        slug__iexact=slug
    ).exclude(pk=instance.pk).exists()

    else:
        slug_exists = model.objects.filter(
        slug__iexact=slug
    ).exists()

    if slug_exists:
        new_slug = slugify(base_title + '-' + generate_random_string(4))
        return generate_unique_slug(
            instance,
            base_title,
            new=new_slug
        )
    return slug
