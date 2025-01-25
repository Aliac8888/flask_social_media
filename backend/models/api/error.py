class EmptyPatchError(ValueError):
    def __init__(self) -> None:
        super().__init__("Patch is empty")
