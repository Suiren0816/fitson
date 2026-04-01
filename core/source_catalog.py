from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterator


@dataclass(slots=True)
class SourceRecord:
    """Single source record for table and CSV output."""

    source_id: int
    x: float
    y: float
    ra: str = "-"
    dec: str = "-"
    flux: float = 0.0
    peak: float = 0.0
    snr: float = 0.0
    a: float = 0.0
    b: float = 0.0
    theta: float = 0.0
    flag: int = 0
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class SourceCatalog:
    """Structured source-catalog container skeleton."""

    records: list[SourceRecord] = field(default_factory=list)

    COLUMN_NAMES = (
        "ID",
        "X",
        "Y",
        "RA",
        "Dec",
        "Flux",
        "Peak",
        "SNR",
        "A",
        "B",
        "Theta",
        "Flag",
    )

    @classmethod
    def from_sep_objects(
        cls,
        objects: Any,
        *,
        x_offset: int = 0,
        y_offset: int = 0,
        wcs: Any = None,
    ) -> "SourceCatalog":
        """Build a catalog from SEP output objects."""

        return cls()

    def __len__(self) -> int:
        """Return the number of records in the catalog."""

        return len(self.records)

    def __getitem__(self, index: int) -> SourceRecord:
        """Return a record by row index."""

        return self.records[index]

    def __iter__(self) -> Iterator[SourceRecord]:
        """Iterate over all source records."""

        return iter(self.records)

    def append(self, record: SourceRecord) -> None:
        """Append a single source record."""

        self.records.append(record)

    def clear(self) -> None:
        """Remove all source records."""

        self.records.clear()

    def to_rows(self) -> list[dict[str, Any]]:
        """Convert the catalog into table/CSV row dictionaries."""

        return []

    def to_csv(self, path: str) -> None:
        """Export the catalog to CSV."""

        pass
