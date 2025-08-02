from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        # This ensures that you can't have two categories with the same name under the same parent.
        unique_together = ('name', 'parent',)
        verbose_name_plural = "Categories"

    def __str__(self):
        # Build a string showing the full path, e.g., "Philosophy > Science Philosophy"
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    # The main cover image for the book
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('bookstore:book_detail', args=[self.id])


class BookImage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='book_images/')

    def __str__(self):
        return f"Image for {self.book.title}"


class SiteSettings(models.Model):
    """
    Site-wide settings that can be configured through the admin panel.
    This model implements a singleton pattern to ensure only one settings record exists.
    """
    cover_image = models.ImageField(
        upload_to='site_settings/', 
        null=True, 
        blank=True,
        help_text="Main cover image for the home page hero section"
    )
    site_title = models.CharField(
        max_length=200, 
        default="المكتبة الجيرمانية",
        help_text="Main site title displayed across the website"
    )
    hero_title = models.CharField(
        max_length=300,
        default="اكتشف كتابك القادم المثالي",
        help_text="Main headline on the home page hero section"
    )
    hero_subtitle = models.TextField(
        default="مجموعة منتقاة من أفضل الكتب لتعلم اللغة الألمانية وتطوير مهارات القراءة",
        help_text="Subtitle text on the home page hero section"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def save(self, *args, **kwargs):
        # Implement singleton pattern - only one settings record allowed
        if not self.pk and SiteSettings.objects.exists():
            # If trying to create a new record when one already exists, update the existing one
            existing = SiteSettings.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Prevent deletion of the settings record
        pass

    def __str__(self):
        return f"Site Settings (Last updated: {self.updated_at.strftime('%Y-%m-%d %H:%M')})"

    @classmethod
    def get_settings(cls):
        """Helper method to get the site settings, creating default if none exist"""
        settings, created = cls.objects.get_or_create(defaults={
            'site_title': "المكتبة الجيرمانية",
            'hero_title': "اكتشف كتابك القادم المثالي",
            'hero_subtitle': "مجموعة منتقاة من أفضل الكتب لتعلم اللغة الألمانية وتطوير مهارات القراءة"
        })
        return settings


# notes
#  on this file iswju os the bookImage model declared but not used at all by other models.
# 