class SimpleEnergyError(Exception):
    """
    Classe base para excessões do projeto.
    """
    pass


class FormatFileError(SimpleEnergyError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.file_format = kwargs.get('file_format')


class ResposeStatusCodeError(SimpleEnergyError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.status_code = kwargs.get('status_code')


class InputCSRFError(SimpleEnergyError):
    pass


class ClientCodeNotFound(SimpleEnergyError):
    pass
