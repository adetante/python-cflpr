from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self


@dataclass
class PRAddress:
    streetAndNumber: str
    city: str
    zipCode: str

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return PRAddress(
            data["streetAndNumber"],
            data["city"],
            data["zipCode"],
        )


@dataclass
class PR:
    id: str
    name: str
    phone: str
    address: PRAddress
    maxHeightInMeters: float
    maxWeightInKg: float
    maxLengthInMeters: float
    status: str
    isIndoor: bool
    hasElectricalSlots: bool
    hasPmrSlots: bool
    hasEnterpriseSlots: bool
    isOpenNightAndDay: bool
    isFlex: bool
    totalSpaces: int
    totalElectricalSpaces: int
    maxEnterpriseSpaces: int
    totalPmrSpaces: int
    occupiedElectricalSpaces: int
    occupiedPmrSpaces: int
    occupiedTotalSpaces: int
    latitude: float
    longitude: float
    isGratuityAvailable: bool
    isOutsidePark: bool

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return PR(
            data["id"],
            data["name"],
            data["phone"],
            PRAddress.from_json(data["address"]),
            data["maxHeightInMeters"],
            data["maxWeightInKg"],
            data["maxLengthInMeters"],
            data["status"],
            data["isIndoor"],
            data["hasElectricalSlots"],
            data["hasPmrSlots"],
            data["hasEnterpriseSlots"],
            data["isOpenNightAndDay"],
            data["isFlex"],
            data["totalSpaces"],
            data["totalElectricalSpaces"],
            data["maxEnterpriseSpaces"],
            data["totalPmrSpaces"],
            data["occupiedElectricalSpaces"],
            data["occupiedPmrSpaces"],
            data["occupiedTotalSpaces"],
            data["latitude"],
            data["longitude"],
            data["isGratuityAvailable"],
            data["isOutsidePark"],
        )


@dataclass
class Ticket:
    id: str
    isActive: bool
    plateNumber: str
    parkAndRideId: str
    parkAndRideName: str
    entryDateTime: datetime
    duration: str
    cost: float
    costToShow: str
    lastPaymentDateTime: datetime | None
    hasToPayExtraCost: bool
    durationToShow: str
    hasGratuityGranted: bool
    hasDetectedDriver: bool
    isOutsideRadius: bool
    exitDateTime: datetime | None
    parkHasGratuityAvailable: bool

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return Ticket(
            data["id"],
            data["isActive"],
            data["plateNumber"],
            data["parkAndRideId"],
            data["parkAndRideName"],
            datetime.fromisoformat(data["entryDateTime"]),
            data["duration"],
            data["cost"],
            data["costToShow"],
            datetime.fromisoformat(data["lastPaymentDateTime"])
            if data["lastPaymentDateTime"] is not None
            else None,
            data["hasToPayExtraCost"],
            data["durationToShow"],
            data["hasGratuityGranted"],
            data["hasDetectedDriver"],
            data["isOutsideRadius"],
            datetime.fromisoformat(data["exitDateTime"])
            if data["exitDateTime"] is not None
            else None,
            data["parkHasGratuityAvailable"],
        )
