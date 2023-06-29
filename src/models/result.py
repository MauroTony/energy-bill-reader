import pydantic

"""
{
    "identificacao": {
        "name": "nome do usuario",
        "nit": 12321312312,
        "birthdate": "10/10/1990",
        "cpf": "131312321312"
    },
    "relacoes": [
        {
            "seq": 1,
            "origin": "nome da empresa",
            "init_date": "10/10/2000",
            "end_date": "10/10/2000",
            "contributions": []
        },
        {
            "seq": 6,
            "origin": "nome da empresa 6",
            "init_date": "10/10/2000",
            "end_date": "10/10/2000",
            "contributions": [
                {
                    "competencia": "01/1982",
                    "value": "141.735,05"
                },
                {
                    "competencia": "04-1982",
                    "value": "141.735,05"
                }
            ]
        }
    ]
}
"""


class Relacao(pydantic.BaseModel):
    seq: int | None = None
    origin: str | None = None
    initDate: str | None = None
    endDate: str | None = None
    contributions: list | None = None


class Contributions(pydantic.BaseModel):
    competencia: str | None = None
    value: str | None = None


class identification(pydantic.BaseModel):
    name: str | None = None
    nit: str | None = None
    birthDate: str | None = None
    cpf: str | None = None
    relations: list | None = []


class Result_final(pydantic.BaseModel):
    beneficiaryId: int | None = None
    data: identification | None = None
    apiName: str | None = None
