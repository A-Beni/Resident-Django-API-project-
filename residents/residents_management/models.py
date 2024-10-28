from django.db import models

class Building(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} at {self.address}"

class Room(models.Model):
    number = models.CharField(max_length=10)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['building', 'number']
        unique_together = ('number', 'building')
    
    def __str__(self):
        return f"{self.number} in {str(self.building)}"

class Resident(models.Model):
    name = models.CharField(max_length=100)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} in {str(self.room)}"