from acp_192_201.Assignment_02.rental import Motorbike, ElectricCar, Vehicle
from acp_192_201.Assignment_02.rental import Renter

def rent_vehicle(renter, vehicle):
    if renter.rented_vehicle is not None:
        print(f"{renter.name} already has a rented vehicle:{renter.rented_vehicle}.")
        return
    if vehicle.is_rented:
        print(f"{vehicle} is already rented.")
        return
    vehicle.rent(renter)
    print(f"{renter.name} has rented {vehicle}.")

def main():
    results = []
    def check(name, fn):
        try:
            fn(); print(f"[PASS] {name}")
        except AssertionError as e:
            print(f"[FAIL] {name}   -> {str(e) or 'assertion failed'}")
        except Exception as e:
            print(f"[FAIL] {name}   -> {type(e).__name__}: {e}"[:80])

    def c1():
        car = Vehicle("Toyota", "Camry", "ABC123")
        assert str(car) == "Toyota Camry (Plate: ABC123) - available"
    check("1. Vehicle __str__ works", c1)

    def c2():
        ev = ElectricCar("Tesla", "Model 3", "XYZ789", 75)
        assert str(ev) == "Tesla Model 3 (Plate: XYZ789) - available"
    check("2. ElectricCar __str__ works", c2)

    def c3():
        mbike = Motorbike("Yamaha", "R1", "MOTO456", 1000)
        assert str(mbike) == "Yamaha R1 (Plate: MOTO456) - available"
    check("3. Motorbike __str__ works", c3)

    def c4():
        renter = Renter("Alice", "D1234567")
        assert renter.name == "Alice"
        assert renter.license_number == "D1234567"
        assert renter.rented_vehicle is None
    check("4. Renter attributes are set correctly", c4)

    def c5():
        car = Vehicle("Toyota", "Camry", "ABC123")
        renter = Renter("Alice", "D1234567")
        rent_vehicle(renter, car)
        assert renter.rented_vehicle == car
        assert car.is_rented is True
    check("5. Vehicle rental works correctly", c5)

    def c6():
        car = Vehicle("Toyota", "Camry", "ABC123")
        renter1 = Renter("Alice", "D1234567")
        renter2 = Renter("Bob", "D7654321")
        rent_vehicle(renter1, car)
        try:
            rent_vehicle(renter2, car)
            assert False, "Allowed renting an already rented vehicle"
        except Exception:
            pass
    check("6. Cannot rent an already rented vehicle", c6)

    def c7():
        car = Vehicle("Toyota", "Camry", "ABC123")
        renter1 = Renter("Alice", "D1234567")
        renter2 = Renter("Bob", "D7654321")
        rent_vehicle(renter1, car)
        try:
            rent_vehicle(renter1, car)
            assert False, "Allowed renting a vehicle when already rented one"
        except Exception:
            pass
    check("7. Cannot rent the same vehicle twice", c7)

    def c8():
        car = Vehicle("Toyota", "Camry", "ABC123")
        renter = Renter("Alice", "D1234567")
        rent_vehicle(renter, car)   
        car.return_vehicle(renter)
        assert renter.rented_vehicle is None
        assert car.is_rented is False   
    check("8. Vehicle return works correctly", c8)

    for result in results:
            print(f"[{'PASS' if result[1] else 'FAIL'}] {result[0]}" + (f"   -> {result[2]}" if not result[1] else ""))

if __name__ == "__main__":
    main()