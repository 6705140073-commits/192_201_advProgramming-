class Vehicle:
    def __init__(self, make, model, plate, is_rented=False):
        self.make = make
        self.model = model
        self.plate = plate
        self.is_rented = is_rented
        self.renter = None

    def rent(self, renter=None):
        if self.is_rented:
            raise Exception(f"{self.make} {self.model} is already rented.")
        if renter is not None and not isinstance(renter, Renter):
            raise ValueError("Renter must be a Renter instance or None.")
        if renter is not None and renter.rented_vehicle is not None and renter.rented_vehicle is not self:
            raise Exception(f"{renter.name} already has a vehicle rented.")

        self.is_rented = True
        self.renter = renter
        if renter is not None:
            renter.rented_vehicle = self

    def return_vehicle(self, renter=None):
        if not self.is_rented:
            raise Exception(f"{self.make} {self.model} is not currently rented.")
        if renter is not None and not isinstance(renter, Renter):
            raise ValueError("Renter must be a Renter instance or None.")
        if renter is not None and self.renter is not None and renter is not self.renter:
            raise Exception(f"{self.make} {self.model} was rented to {self.renter.name}.")

        if self.renter is not None:
            self.renter.rented_vehicle = None

        self.renter = None
        self.is_rented = False

    def __str__(self):
        return f"{self.make} {self.model} (Plate: {self.plate}) - {'rented' if self.is_rented else 'available'}"

class Renter:
    def __init__(self, name, license_number, rented_vehicle=None):
        if name is None:
            raise ValueError("Name cannot be Empty.")
        else:
            self.name = name
        if license_number is None:
            raise ValueError("License number cannot be Empty.")
        else:
            self.license_number = license_number
        self.rented_vehicle = rented_vehicle

    @property
    def rented_vehicle(self):
        return self._rented_vehicle

    @rented_vehicle.setter
    def rented_vehicle(self, value):
        if value is not None and not isinstance(value, Vehicle):
            raise ValueError("Rented vehicle must be a Vehicle instance or None.")
        self._rented_vehicle = value

class ElectricCar(Vehicle):
    def __init__(self, make, model, plate, battery_capacity, is_rented=False):
        super().__init__(make, model, plate, is_rented)

        if not isinstance(battery_capacity, (int, float)) or battery_capacity <= 0:
            raise ValueError("Battery capacity must be a positive number.")

        self.battery_capacity = battery_capacity

    # def charge(self):
    #     print(f"{self.make} {self.model} is charging.")

    # def __str__(self):
    #     return f"{super().__str__()} - Battery Capacity: {self.battery_capacity} kWh"

class Motorbike(Vehicle):
    def __init__(self, make, model, plate, engine_capacity, is_rented=False):
        super().__init__(make, model, plate, is_rented)
        if not isinstance(engine_capacity, (int, float)) or engine_capacity <= 0:
            raise ValueError("Engine capacity must be a positive number.")

        self.engine_capacity = engine_capacity

    # def rev_engine(self):
    #     """Return a status message indicating that the engine is revving."""
    #     return f"{self.make} {self.model} is revving its engine."

    # def __str__(self):
    #     return f"{super().__str__()} - Engine Capacity: {self.engine_capacity} cc"