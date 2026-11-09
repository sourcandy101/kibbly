"""The storage interface. Every implementation validates documents against the contract before writing."""

from kibbly_ai import contracts


class Storage:
    """Collections and documents, as in Firestore. Collection names come from contracts.COLLECTIONS."""

    name = "base"

    def put(self, collection: str, document: dict) -> str:
        """Validate and save a document (insert or replace). Returns its id."""
        contracts.validate(collection, document)
        doc_id = document[contracts.id_field(collection)]
        self._write(collection, doc_id, document)
        return doc_id

    def get(self, collection: str, doc_id: str):
        """Return the document, or None if it does not exist."""
        raise NotImplementedError

    def query(self, collection: str, **equals) -> list:
        """Return every document whose fields equal the given values, for example query("meals", dog_id="dog_mochi")."""
        raise NotImplementedError

    def _write(self, collection: str, doc_id: str, document: dict) -> None:
        raise NotImplementedError
