from django.db import models
from datetime import date
# Create your models here.


class VehicleType(models.Model):
    name = models.CharField(max_length=32)
    max_capacity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=32)
    passengers = models.PositiveIntegerField()
    vehicle_type = models.ForeignKey(VehicleType, null=True, on_delete=models.SET_NULL)
    number_plate = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name

    def can_start(self) -> bool:
        return self.vehicle_type.max_capacity >= self.passengers
    
    def get_distribution(self) -> list:
        if self.vehicle_type:
            max_capacity = self.vehicle_type.max_capacity
            distribution_lineal = [ x <= self.passengers  for x in range(1, max_capacity + 1)]
            distribution_group = []
            for y in range(round(max_capacity / 2.0)):
                distribution_group.append(distribution_lineal[y*2: (y+1) * 2])
            return distribution_group
        return []

class Journey(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.vehicle.name} ({self.start} - {self.end})"

    def is_finished(self) -> bool:
        if not self.end:
            return False
        return self.end <= date.today()


def validate_number_plate(number_plate: str) -> bool:
    number_plate_list = number_plate.split("-")
    if not len(number_plate_list) == 3:
        return False
    is_first_letter = number_plate_list[0].isalpha()
    is_second_number = number_plate_list[1].isdigit()
    is_third_number = number_plate_list[2].isdigit()
    return all([is_first_letter, is_second_number, is_third_number])