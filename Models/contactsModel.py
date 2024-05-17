# generated by datamodel-codegen:
#   filename:  personSchema.json
#   timestamp: 2024-05-15T14:34:50+00:00

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class Address(BaseModel):
    city: str
    country: str
    countryCode: str
    extendedAddress: str
    poBox: str
    postalCode: str
    region: str
    streetAddress: str
    type: str


class AgeRange(BaseModel):
    ageRange: str


class Biography(BaseModel):
    contentType: str
    value: str


class Date(BaseModel):
    day: int
    month: int
    year: int


class Birthday(BaseModel):
    date: Date
    text: str


class ClientDatum(BaseModel):
    key: str
    value: str


class CoverPhoto(BaseModel):
    default: bool
    url: str


class EmailAddress(BaseModel):
    displayName: str
    type: str
    value: str


class Event(BaseModel):
    date: Date
    type: str


class ExternalId(BaseModel):
    type: str
    value: str


class FileAse(BaseModel):
    value: str


class Gender(BaseModel):
    addressMeAs: str
    value: str


class ImClient(BaseModel):
    protocol: str
    type: str
    username: str


class Interest(BaseModel):
    value: str


class Locale(BaseModel):
    value: str


class Location(BaseModel):
    buildingId: str
    current: bool
    deskCode: str
    floor: str
    floorSection: str
    type: str
    value: str


class MiscKeyword(BaseModel):
    type: str
    value: str


class Name(BaseModel):
    familyName: str
    givenName: str
    honorificPrefix: str
    honorificSuffix: str
    middleName: str
    phoneticFamilyName: str
    phoneticFullName: str
    phoneticGivenName: str
    phoneticHonorificPrefix: str
    phoneticHonorificSuffix: str
    phoneticMiddleName: str
    unstructuredName: str


class Nickname(BaseModel):
    type: str
    value: str


class Occupation(BaseModel):
    value: str


class EndDate(BaseModel):
    day: int
    month: int
    year: int


class StartDate(BaseModel):
    day: int
    month: int
    year: int


class Organization(BaseModel):
    costCenter: str
    current: bool
    department: str
    domain: str
    endDate: EndDate
    fullTimeEquivalentMillipercent: int
    jobDescription: str
    location: str
    name: str
    phoneticName: str
    startDate: StartDate
    symbol: str
    title: str
    type: str


class PhoneNumber(BaseModel):
    type: str
    value: str


class Photo(BaseModel):
    default: bool
    url: str


class Relation(BaseModel):
    person: str
    type: str


class SipAddress(BaseModel):
    type: str
    value: str


class Skill(BaseModel):
    value: str


class Url(BaseModel):
    type: str
    value: str


class UserDefinedItem(BaseModel):
    key: str
    value: str


class ContactsModel(BaseModel):
    addresses: Optional[List[Address]] = None
    ageRanges: Optional[List[AgeRange]] = None
    biographies: Optional[List[Biography]] = None
    birthdays: Optional[List[Birthday]] = None
    clientData: Optional[List[ClientDatum]] = None
    coverPhotos: Optional[List[CoverPhoto]] = None
    emailAddresses: Optional[List[EmailAddress]] = None
    events: Optional[List[Event]] = None
    externalIds: Optional[List[ExternalId]] = None
    fileAses: Optional[List[FileAse]] = None
    genders: Optional[List[Gender]] = None
    imClients: Optional[List[ImClient]] = None
    interests: Optional[List[Interest]] = None
    locales: Optional[List[Locale]] = None
    locations: Optional[List[Location]] = None
    miscKeywords: Optional[List[MiscKeyword]] = None
    names: List[Name]
    nicknames: Optional[List[Nickname]] = None
    occupations: Optional[List[Occupation]] = None
    organizations: Optional[List[Organization]] = None
    phoneNumbers: Optional[List[PhoneNumber]] = None
    photos: Optional[List[Photo]] = None
    relations: Optional[List[Relation]] = None
    sipAddresses: Optional[List[SipAddress]] = None
    skills: Optional[List[Skill]] = None
    urls: Optional[List[Url]] = None
    userDefined: Optional[List[UserDefinedItem]] = None

class BodyModel(BaseModel):
    resourceName: Optional[str] = Field(...,description="The resource name for the person, assigned by the server. An ASCII string in the form of `people/{person_id}`. (only required for peoleUpdate)")
    body: List[ContactsModel] = None