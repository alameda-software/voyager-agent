from app.models import ConciergeDomain

from app.domains.base import DomainPack
from app.domains.voyager.pack import voyager_pack
from app.domains.wedding.pack import wedding_pack


DOMAIN_PACKS: dict[ConciergeDomain, DomainPack] = {
    ConciergeDomain.VOYAGER: voyager_pack,
    ConciergeDomain.WEDDING: wedding_pack,
}


def get_domain_pack(domain: ConciergeDomain) -> DomainPack:
    return DOMAIN_PACKS[domain]
