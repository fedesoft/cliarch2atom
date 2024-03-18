from dataclasses import dataclass

@dataclass(slots=True)
class CSVAuthorityRecord:
    culture: str = 'es'
    typeOfEntity: str = ''
    authorizedFormOfName: str = ''
    parallelFormsOfName: str = ''
    standardizedFormsOfName: str = ''
    otherFormsOfName: str = ''
    corporateBodyIdentifiers: str = ''
    datesOfExistence: str = ''
    history: str = ''
    places: str = ''
    legalStatus: str = ''
    functions: str = ''
    mandates: str = ''
    internalStructures: str = ''
    generalContext: str = ''
    descriptionIdentifier: str = ''
    institutionIdentifier: str = ''
    rules: str = ''
    status: str = ''
    levelOfDetail: str = ''
    revisionHistory: str = ''
    sources: str = ''
    maintenanceNotes: str = ''
    actorOccupations: str = ''
    actorOccupationNotes: str = ''
    subjectAccessPoints: str = ''
    placeAccessPoints: str = ''
    digitalObjectPath: str = ''
    digitalObjectURI: str = ''
    xClasificacion: str = ''                # extra1
    xLevel: str = ''                        # extra2
    xIDMSSQL: str = ''                      # extra3


    def __str__(self):
        return f"""{self.typeOfEntity} 
                    || {self.authorizedFormOfName=} 
                    || {self.history=} 
        """
