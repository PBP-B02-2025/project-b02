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
    recommended_size = models.CharField(max_length=5, null = True, blank = True)

    def __str__(self):
        return f"{self.user.username} - {self.recommended_size or 'Belum dihitung'}"
    
    def calculate_bmi(self) :
        bmi = self.weight / ((self.height / 100) ** 2)

        if (bmi < 18.5) :
            self.recommended_size = "S"
        elif (bmi < 25) :
            self.recommended_size = "M"
        else :
            self.recommended_size = "L"

        if (self.waist is not None) :
            if (self.waist > 95) :
                self.recommended_size = "L"

            elif (self.waist < 75):
                self.recommended_size = "S"

        if (self.chest is not None) :
            if (self.chest > 100):
                self.recommended_size = "L"
            elif (self.chest  < 85 and self.recommended_size == "M") :
                self.recommended_size = "S"

        if (self.hip is not None) :
            if (self.hip > 105) :
                self.recommended_size = "L"
            elif (self.hip < 85 and self.recommended_size == "M") :
                self.recommended_size = "S"
        
        self.save()
        