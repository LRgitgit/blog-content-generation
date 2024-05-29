from django.db import models

# A model in Django is a Python class that subclasses django.db.models.Model. Each attribute of the model represents a database field.
# Eg.
# class MyModel(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name

class BlogArticle(models.Model):
    search_intent = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    plan = models.JSONField(blank=True)  # Using JSONField for list of items
    guidance = models.TextField(blank=True)
    intro = models.TextField(blank=True)
    outro = models.TextField(blank=True)
    paragraphs = models.JSONField(blank=True)  # Using JSONField for list of paragraphs

    stable_prompt = models.TextField(blank=True)
    img_title = models.CharField(max_length=255, blank=True)
    jpg_name = models.CharField(max_length=255, blank=True)
    img_alt = models.CharField(max_length=255, blank=True)

    nearest_title = models.CharField(max_length=255, blank=True)
    nearest_title_CTA = models.CharField(max_length=255, blank=True)
    backlink_slug = models.CharField(max_length=255, blank=True)
    
    book_title = models.CharField(max_length=255, blank=True)
    book_CTA = models.CharField(max_length=255, blank=True)
    book_link = models.URLField(blank=True)
    book_description = models.TextField(blank=True)

    bold_list = models.JSONField(blank=True)  # Using JSONField for list of bold items

    yt_id = models.CharField(max_length=255, blank=True)
    yt_title = models.CharField(max_length=255, blank=True)
    yt_url = models.URLField(blank=True)

    slug = models.SlugField(unique=True, blank=True)

    # Define what is printed instead of the article instance
    def __str__(self):
        return self.search_intent