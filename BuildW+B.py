# TODO see if dictionaries will support math with units


# Constants:
JetA = 6.75   # Lbs/gal
AVGAS100LL = 6.00   # Lbs/gal
DatumPlane = 0.00  # This is the reference for all arm measurements In


class CalculationError(Exception):
    pass


class StationMake:
    def __init__(self):
        self.Weight = None
        self.Arm = None
        self.MaxWeight = None
        self.FuelGrade = None
        self.UsableFuelVolume = None
        self.Weight = None
        self.Moment = None
        self.Checks = []
        self.OverloadDifference = None

    def setval(self, arm, weight=None, max_weight=None, fuel_grade=None, usable_fuel_volume=None):
        self.Weight = weight
        self.Arm = arm
        self.MaxWeight = max_weight
        # Station specific
        if usable_fuel_volume and fuel_grade is not None:
            self.FuelGrade = fuel_grade
            self.UsableFuelVolume = usable_fuel_volume
            self.Weight = fuel_grade * usable_fuel_volume
        # Moment is put here because it needs to take into account the updated Weight value
        self.Moment = self.Weight * arm
        # The chunk below ensures self.weight is within limits
        if self.MaxWeight is not None:  # This is useful for filtering out a station that doesn't have a weight limit
            if self.Weight <= self.MaxWeight:
                self.Checks.append("Weight = pass")
            elif self.Weight > self.MaxWeight:
                self.OverloadDifference = self.MaxWeight - self.Weight
                print("Station weight exceeds max weight!")
                print("Try shifting or removing", self.OverloadDifference, " lbs.")
                # ToDo: Implement weight shift feature
            else:
                raise CalculationError("Calculator unreliable (error should not be raised during normal operation)")

    def print_attributes(self): # This function is for debugging
        print(self)
        if self.FuelGrade and self.UsableFuelVolume is not None:
            print("Fuel grade: ", self.FuelGrade)
            print("Usable fuel volume: ", self.UsableFuelVolume)
        print("Weight: ", self.Weight)
        print("Weight limit: ", self.MaxWeight)
        print("Arm: ", self.Arm)
        print("Moment: ", self.Moment)


class Cessna150GMake:
    def __init__(self):
        # Constants of the airplane model
        self.Load = 0    # This is the sum of all weight of the airplane
        self.Moment = 0    # This is the default value for the moment of the loaded plane
        self.MaxGrossWeight = 1600.00  # Lbs
        # self.ServiceCeiling = 12650  # Ft
        self.MaxBaggage = 120  # Lbs
        # self.WingLoad = 10.2  # Lbs/ft**2 (see if this is a constant of is adjusted based on W+B)
        # self.PowerLoading = 16.0  # Lbs/hp (see if this is a constant of is adjusted based on W+B)
        self.MaxOil = 6  # Qt
        # self.Propeller = {"type": "fixed pitch", "diameter": 69}    # In
        # self.Engine = "Continental O-200-A"  # Carburated, Opposed, 200 in**3 displacement, model A.
        # http://www.tcmlink.com/pdf2/SIL05-3A.pdf
        # self.Wingspan = 392.5    # In
        # self.Length = 285   # In
        # self.Height = 103.5    # In
        # Fuel Volumes
        # Standard
        self.MaxStandardFuelTanks = 26  # Gal
        self.MaxStandardUsableFuel = 22.5  # Gal
        self.StandardUnusableFuel = 3.5  # Gal
        # Long Range
        self.MaxLongRangeFuelTanks = 38  # Gal
        self.MaxLongRangeUsableFuel = 35.0  # Gal
        self.LongRangeUnusableFuel = 3.0  # Gal
        self.TypeCertificate = "3A19"    # https://150cessna.tripod.com/3a19.pdf
        self.Category = "Utility"
        self.Stations = ["BasicEmpty", "Passengers", "ForeCargo", "AftCargo", "FuelTanks"]

        # Empty variables that are airplane specific
        # self.EquipmentList = []  # Used only as an exercise to find equipment list
        self.Warnings = []  # Used to warn of low tolerances

    # def total_weight(self):
    #     for i in range(len(self.Stations)):
    #         self.Load += self.Stations[i]
    #     return self.Load

    def total_moment(self):
        pass

    # Test area

    # def cruise_speed(self):
    #     pass

    # def range(self):
    #     pass

    # def rate_of_climb(self):
    #     pass

    # def takeoff(self):
    #     pass

    # def landing(self):
    #     pass


class Cessna152Make:
    pass

# Empty Weight notes
# Licensed Empty Weight = airframe + engine(s) + unusable fuel + undrainable oil + standard + optional equipment
    # according to equipment list
# Standard Empty Weight = airframe + engine(s) + fixed and permanent operating equipment like fixed ballast hydraulic
    # fluid usable and full engine oil
# Basic Empty Weight = standard empty weight + weight of optional and special equipment installed


# Aircraft specific details

# The chunk of code below creates station objects based on the pre-set constant varies and user input variables. This
# section is just for assigning and computing attributes of hte stations.
# ToDo: fix the assignment of the stations so that the obj name is pulled form the N3038S.Stations attribute. This will
#  help with scaling
N3038S = Cessna150GMake()
N3038S.Stations = ["BasicEmpty", "Passengers", "ForeCargo", "AftCargo", "FuelTanks"] # Try to move this to
# Cessna150GMake.__init__()
for i in range(len(N3038S.Stations)):
    N3038S.Stations[i] = StationMake()

N3038S.Stations[0].setval(34.23, 1050.00)    # Basic empty
N3038S.Stations[1].setval(39.00, int(input("Pilot weight: ")) + int(input("Copilot weight: ")))   # Passengers
N3038S.Stations[2].setval(64.00, int(input("Fore cargo weight: ")), 120)  # Fore cargo
N3038S.Stations[3].setval(84.00, int(input("Aft cargo weight: ")), 40)  # Aft cargo
N3038S.Stations[4].setval(40.00, fuel_grade=int(input("What fuel grade is being used? ")), usable_fuel_volume=int(
    input("How many gallons of usable fuel? ")))    # Fuel tanks

for i in range(len(N3038S.Stations)):
    N3038S.Load += N3038S.Stations[i].Weight
    N3038S.Moment += N3038S.Stations[i].Moment

print(N3038S.Load)
print(N3038S.Moment)

N3038S.CenterOfGravity = N3038S.Load/N3038S.Moment
N3038S.CenterOfGravityEnvelope = (32.9, 37.5)  # Inches
if 32.9 <= N3038S.CenterOfGravity <= 37.5:


# CenterGravity = "add me"


# def weight_check():
#
#     def gross():  # Checks total loading
#         if TotalWeight < MaxGross:
#             # Add a list of CheckedItems for display in green/red if function passed/failed
#             pass
#         elif TotalWeight == MaxGross:
#             Warnings.append("CAUTION: AIRCRAFT AT MAX GROSS WEIGHT")
#             return Warnings
#         elif TotalWeight > MaxGross:
#             raise Exception("W+B failed: Max gross weight surpassed")
#         else:
#             sys.exit("Max_Weight_Check failed. Calculator in-op")
#
#     def station_2():  # Checks fore loading
#         if Station2Weight < Station2MaxWeight:
#             # Add a list of CheckedItems for display in green/red if function passed/failed
#             pass
#         elif Station2Weight == Station2MaxWeight:
#             Warnings.append("CATION: FORE CARGO AT MAX LOAD")
#             return Warnings
#         elif Station2Weight > Station2MaxWeight:
#             raise Exception("W+B failed: Max fore cargo load exceeded")
#         else:
#             sys.exit("Station_2_Weight_Check failed. Calculator in-op")
#
#     def station_3():   # Checks aft loading
#         if Station3Weight < Station3MaxWeight:
#             # Add a list of CheckedItems for display in green/red if function passed/failed
#             pass
#         elif Station3Weight == Station3MaxWeight:
#             Warnings.append("CATION: AFT CARGO AT MAX LOAD")
#             return Warnings
#         elif Station3Weight > Station3MaxWeight:
#             raise Exception("W+B failed: Max aft cargo load exceeded")
#         else:
#             sys.exit("Station_3_Weight_Check failed. Calculator in-op")
#
#     def cargo():
#         max_cargo = 120
#         cargo_total = Station2Weight + Station3Weight
#         if cargo_total < max_cargo:
#             # Add a list of CheckedItems for display in green/red if function passed/failed
#             pass
#         elif cargo_total == max_cargo:
#             Warnings.append("CAUTION: Max cargo loading")
#             return Warnings
#         elif cargo_total > max_cargo:
#             raise Exception("W+B failed:cargo loading exceeded")
#        else:
#            sys.exit("cargo failed. Calculator not functional")
#
#     gross()
#     station_2()
#     station_3()
#     cargo()


# def envelope_check():
#     # This function will determine if the total moment and weight fall within bounds
#     pass

# range vs payload optimizer

# Aircraft specific details
N355AA = Cessna152Make()

