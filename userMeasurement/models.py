from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class userMeasurement(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    height = models.FloatField(help_text="Height in centimeters")
    weight = models.FloatField(help_text="Weight in kilograms")
    waist = models.FloatField(help_text="(Optional) Waist in centimeters", null = True, blank = True)
    hip = models.FloatField(help_text="(Optional) Hip in centimeters", null = True, blank = True)
    chest = models.FloatField(help_text = "(Optional) Chest in centimeters", null = True, blank = True)
    head_circumference = models.FloatField(help_text="Head circumference in centimeters")
    clothes_size = models.CharField(max_length=5, null = True, blank = True)
    helmet_size = models.CharField(max_length=5, null = True, blank = True)
    def __str__(self):
        return f"{self.user.username} - {self.recommended_size or 'Belum dihitung'}"
    
    def calculate_clothes_size(self):
        bmi = self.weight / ((self.height / 100) ** 2)
        
        size = "M"  # default

        if bmi < 18.5:
            size = "S"
        elif bmi < 25:
            size = "M"
        elif bmi < 30:
            size = "L"
        else:
            size = "XL"

        # Adjust based on waist
        if self.waist is not None:
            if self.waist < 75:
                size = "S"
            elif self.waist > 95 and self.waist <= 105:
                size = "L"
            elif self.waist > 105:
                size = "XL"

        # Adjust based on chest
        if self.chest is not None:
            if self.chest < 85 and size in ["M", "L"]:
                size = "S"
            elif self.chest > 100 and self.chest <= 110:
                size = "L"
            elif self.chest > 110:
                size = "XL"

        # Adjust based on hip
        if self.hip is not None:
            if self.hip < 85 and size in ["M", "L"]:
                size = "S"
            elif self.hip > 105 and self.hip <= 115:
                size = "L"
            elif self.hip > 115:
                size = "XL"

        self.clothes_size = size
        self.save()

    def calculate_helmet_size(self):
        hc = self.head_circumference
        if hc is None:
            self.helmet_size = None
        elif hc < 54:
            self.helmet_size = "XS"
        elif hc <= 56:
            self.helmet_size = "S"
        elif hc <= 59:
            self.helmet_size = "M"
        elif hc <= 62:
            self.helmet_size = "L"
        else:
            self.helmet_size = "XL"

        self.save()
        