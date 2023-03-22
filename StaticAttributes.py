class Cessna150GMake:
    def __init__(self):
        self.BasicEmpty = None
        self.Passengers = None
        self.Fuel = None
        self.BaggageFore = None
        self.BaggageAft = None
        self.BaggageCombined = None     # Used to ensure there is <= 120 lbs in fore and aft
        self.Total = None

    class BasicEmpty:
        def __init__(self):
            self.Weight = None
            self.Arm = None
            self.Moment = self.Weight * self.Arm

    class Passengers:
        def __init__(self):
            self.LeftSeat = None
            self.RightSeat = None
            self.Weight = self.LeftSeat + self.RightSeat
            self.Arm = None
            self.Moment = self.Weight * self.Arm

    class Fuel:
        def __init__(self):
            self.Volume = None  # This is the volume of usable fuel
            self.Type = None
            self.Weight = self.Volume * self.Type
            self.Arm = None
            self.Moment = self.Weight * self.Arm

    class BaggageFore:
        def __init__(self):
            i = 0
            self.ItemNumber = 3
            self.Items = []
            self.Weight = None
            self.Arm = None
            self.Moment = self.Weight * self.Arm
            while i < self.ItemNumber:
                self.Items.append("User input here")
                i += 1

    class BaggageAft:
        def __init__(self):

            self.Weight = None
            self.Arm = None
            self.Moment = self.Weight * self.Arm

    class BaggageCombined:
        def __init__(self):

            self.Weight = None
            self.Arm = None
            self.Moment = self.Weight * self.Arm


# Max gross weight
# Basic empty weight
# Datum plane is set to 0in
# Fuel tank size and arm
# Passenger seats (edit to allow for different configs)
# Max loading for all stations
