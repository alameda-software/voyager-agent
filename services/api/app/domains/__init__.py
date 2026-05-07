"""
Domain packs for concierge modes.

Each domain should own its prompts, schemas, fake providers, ranking rules,
and presentation adapters so it can later move into its own repository.
"""

from app.domains.registry import get_domain_pack

__all__ = ["get_domain_pack"]
