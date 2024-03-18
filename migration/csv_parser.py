from dataclasses import dataclass

@dataclass(slots=True)
class CSVDescription:
    legacyId: str = ""
    parentId: str = ""
    qubitParentSlug: str = ""               # manual slug
    accessionNumber: str = ""
    identifier: str = ""                    # ee
    title: str = ""                         # ff
    levelOfDescription: str = ""            # gg
    extentAndMedium: str = ""               # hh
    repository: str = ""                    # ii
    archivalHistory: str = ""               # jj
    acquisition: str = ""                   # kk
    scopeAndContent: str = ""               # ll
    appraisal: str = ""                     # mm
    accruals: str = ""                      # nn
    arrangement: str = ""
    accessConditions: str = ""              # pp
    reproductionConditions: str = ""        # qq
    language: str = ""
    script: str = ""
    languageNote: str = ""
    physicalCharacteristics: str = ""         # uu
    findingAids: str = ""                     # vv
    locationOfOriginals: str = ""             # ww
    locationOfCopies: str = ""                # xx
    relatedUnitsOfDescription: str = ""       # yy
    publicationNote: str = ""                 # zz
    digitalObjectPath: str = ""
    digitalObjectURI: str = ""
    generalNote: str = ""                     # aac
    subjectAccessPoints: str = ""             # aad
    placeAccessPoints: str = ""               # aae
    nameAccessPoints: str = ""
    genreAccessPoints: str = ""
    descriptionIdentifier: str = ""
    institutionIdentifier: str = ""
    rules: str = ""
    descriptionStatus: str = ""
    levelOfDetail: str = ""
    revisionHistory: str = ""
    languageOfDescription: str = ""
    scriptOfDescription: str = ""
    sources: str = ""
    archivistNote: str = ""
    publicationStatus: str = ""
    physicalObjectName: str = ""
    physicalObjectLocation: str = ""
    physicalObjectType: str = ""
    alternativeIdentifiers: str = ""
    alternativeIdentifierLabels: str = ""
    eventDates: str = ""                    # aax
    eventTypes: str = ""
    eventStartDates: str = ""
    eventEndDates: str = ""
    eventActors: str = ""                   # bbb
    eventActorHistories: str = ""
    culture: str = 'es'
    xClasificacion: str = ""                # extra1
    xLevel: str = ""                        # extra2
    xIDMSSQL: str = ""                      # extra3


    def __str__(self):
        return f"""{self.qubitParentSlug} 
                    || {self.identifier=} 
                    || {self.title=} 
                    || {self.repository=}
                    || {self.levelOfDescription=}
                    || {self.extentAndMedium=}
                    || {self.placeAccessPoints=}
                    || {self.subjectAccessPoints=}
                    || {self.scopeAndContent=}
                    || {self.relatedUnitsOfDescription=}
                    || {self.acquisition=}
                    || {self.appraisal=}
                    || {self.accessConditions=}
                    || {self.reproductionConditions=}
                    || {self.physicalCharacteristics=}
                    || {self.findingAids=}
                    || {self.locationOfOriginals=}
                    || {self.locationOfCopies=}
                    || {self.publicationNote=}
                    || {self.generalNote=}
                    || {self.eventDates=}
        """
