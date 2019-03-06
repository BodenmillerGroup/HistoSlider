class Loader:

    @classmethod
    def load(cls, slide: "Slide"):
        raise NotImplementedError

    @classmethod
    def close(cls, slide: "Slide"):
        raise NotImplementedError
